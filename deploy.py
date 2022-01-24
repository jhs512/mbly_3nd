import os, sys
import locale
import subprocess
import time
import socket
from datetime import datetime
from pathlib import Path


def make_globals():
    global project_dir, docker_work_dir, project_dir_core

    project_name = os.environ.get("JOB_NAME") or "python__2"
    project_dir_core = f"/data/site_projects/{project_name}"

    # 윈도우에서 테스트용 설정입니다.
    if get_sys() == "Win":
        project_dir = '.'
    else:
        project_dir = f"/docker_projects/nginx__1{project_dir_core}/src"

    docker_work_dir = "/usr/src/app"


def deploy():
    global project_dir, docker_work_dir, project_dir_core
    build_id = os.environ.get('BUILD_NUMBER') or get_now()
    path = get_setting_path()
    # 초기 실행 변수
    init = False

    if get_sys() == "Win":
        python = "python"
    else:
        python = "python3"

    # 꼭 본인의 경로에 맞게 수정해주세요!#
    requirements_path = "requirements/prod.txt"
    # 호스트의 절대주소+빌드이름을 받습니다.(도커소켓을 연결해놔서 연동이됨)
    # 도커컨테이너 안의 프로젝트 폴더입니다.
    volume_link = f"{project_dir}:{docker_work_dir}"

    image_name = "python1"

    deploy_con_name = "python__2"
    test_con_name = "python__2__test"
    database_con_name = "mariadb__1"

    test_port = "8001"
    deploy_port = "8000"
    #
    execute_file = "manage.py"
    deploy_setting_file = f"{path}.settings.prod"
    cur_image_name = f"{image_name}:{build_id}"

    deploydockerfile = "dockerfile"
    deploylogfile = "deploy_log_file.txt"

    make_deploy_logs(deploylogfile)

    print("0.DB컨테이너 확인")
    try:
        db_con = Container(get_specific_container(f"{database_con_name}"))
        if connection_checker(db_con, 1) == False:
            raise Exception("DB 컨테이너 연결 실패")
    except:
        raise Exception("DB 컨테이너 연결 실패")
    revise_dockerfile(execute_file, requirements_path, deploydockerfile)

    print("1.배포용 컨테이너 확인")
    try:
        prev_con = Container(get_specific_container(f"{deploy_con_name}"))
    except:
        init = True

    print("2.남아있는 테스트 컨테이너 삭제")
    try:
        shut_con = Container(get_specific_container(f"{test_con_name}"))
        shut_img_con(shut_con.container_name, shut_con.image_name)
    except:
        pass

    print("3.테스트용 이미지 생성")
    os.system("docker pull python:3.10")
    result = get_logs(f"docker build --force-rm -t {cur_image_name} .")
    fail_checker(result, test_con_name, cur_image_name, deploylogfile, "이미지 빌드 실패 requirements 혹은 test를 확인해주세요")

    print("4.make_Test_Con_And_Test")
    result = get_logs(f"docker run -d -p {test_port}:{test_port} --name {test_con_name} {cur_image_name} gunicorn --bind 0:{test_port} {path}.wsgi")
    fail_checker(result, test_con_name, cur_image_name, deploylogfile, "컨테이너 빌드 실패 requirements에 gunicorn이 설치 되어있는지 확인 해 주세요")

    print("5.테스트 컨테이너 실행 확인")
    con_info = get_specific_container(f"{test_con_name}")
    try:
        test_con = Container(con_info)
    except:
        shut_img_con(test_con_name, cur_image_name)
        raise Exception("테스트 컨테이너 실행이 실패했습니다. requirements나 setting을 확인해주세요")

        # print("6.컨테이너 네트워크 연결 테스트")
        # if connection_checker(test_con,10) == False:
        #     shut_img_con(test_con.container_name,cur_image_name)
        raise Exception("테스트 컨테이너 연결 실패")
    else:  ##connection check success
        os.system(f"docker rm -f {test_con.container_name}")
        if init == False:  ##첫실행이 아닐시
            shut_img_con(prev_con.container_name, prev_con.image_name)
            #
        print("7.배포컨테이너 생성")
        print(f"docker run -d -p {deploy_port}:{deploy_port} --name {deploy_con_name}" +
              f" -v {volume_link}" +
              f" --restart unless-stopped {cur_image_name}" +
              f" gunicorn --bind 0:{deploy_port} {path}.wsgi")
        os.system(f"docker run -d -p {deploy_port}:{deploy_port} --name {deploy_con_name}" +
                  f" -v {volume_link}" +
                  f" --restart unless-stopped"
                  f" {cur_image_name}" +
                  f" gunicorn --bind 0:{deploy_port} {path}.wsgi")

        print("8.마이그레션")
        os.system(f"docker exec {deploy_con_name} {python} {execute_file} migrate --settings={deploy_setting_file}")
        os.system(f'docker exec {deploy_con_name} bash -c "echo yes | {python} {execute_file} collectstatic"')

        # messagr success##
        print(" ")  #
        print("Build Succeed")
        print("Container Info")
        get_specific_container(f"{deploy_con_name}")
    try:
        os.remove(f"{deploylogfile}")
    except:
        pass
    try:
        os.remove(f"{deploydockerfile}")
    except:
        pass


class Container:
    def __init__(self, con):
        self.container_name = con[0]
        self.image_name = con[2]
        self.ip = con[-1]
        self.port = con[-2]


def get_sys():
    """
    get_os_name
    """
    global os_encoding
    os_encoding = locale.getpreferredencoding()
    if os_encoding.upper() == 'cp949'.upper():
        return "Win"
    elif os_encoding.upper() == 'UTF-8'.upper():
        return "Lin"


def get_logs(cmd):
    """
    get_logs_from_command
    """
    os_encoding = locale.getpreferredencoding()
    if os_encoding.upper() == 'cp949'.upper():  # Windows
        return subprocess.Popen(
            cmd, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
    elif os_encoding.upper() == 'UTF-8'.upper():  # Mac&Linux
        return os.popen(cmd).read()
    else:
        print("None matched")
        exit()


def get_ports_from_strings(_result, words):
    """
    parse_ports_from_logs
    """
    try:
        tcp = words[-2].split("->")
        _tcp = ""
        for strings in tcp:
            if "tcp" in strings:
                _tcp = strings
                break
        return _tcp.split("/")[0]
    except:
        return ""


def get_docker_containers():
    """
    parse_containers_informations
    """
    cmd = "docker ps -a"
    logs = get_logs(cmd).split("\n")
    column = logs.pop(0)
    result = []
    if logs:
        for line in logs:
            words = line.split("  ")

            while '' in words:
                words.remove('')

            for i in range(len(words)):
                words[i] = words[i].strip().strip()
            try:
                status = words[4].strip().split(" ")[0]
                # print(f"C Name :: {words[-1]}, C ID :: {words[0]}, Img Name :: {words[1]} , Status :: {status}")
                _result = [words[-1], words[0], words[1], status]
                # get ports
                _result.append(get_ports_from_strings(_result, words))
                # get ip
                _result.append(get_logs(
                    "docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + words[0]).strip("'").strip("\n"))
            except:
                pass
            result.append(_result)
    else:
        print("No Containers")
    return result


def get_specific_container(cmd):
    """
    get_specific_container
    """
    a = get_docker_containers()
    for i in a:
        if i[0] == cmd:
            print(f"컨테이너이름 : {i[0]}")
            print(f"이미지이름   : {i[2]}")
            print(f"내부ip주소   : {i[5]}")
            print(f"포트주소     : {i[4]}")
            print(f"현재상태     : {i[3]}")
            return i
    return []


def get_now():
    """
    make a string by current time
    """
    now = datetime.now()
    nows = [now.year, now.month, now.day, now.hour, now.minute, now.second]
    nowtime = ""
    for i in nows:
        nowtime = nowtime + str(i).zfill(2)
    return nowtime


def connection_checker(test_con, counter):
    """
    check container's network
    put container instance
    """
    osType = get_sys()
    print(f"현재 os 타입 :{osType}")
    if osType == "Lin":
        myip = '172.17.0.1'
    else:
        myip = socket.gethostbyname(socket.gethostname())
    print(f"네트워크 연결 준비")
    print(f"로컬IP주소   :{myip}")
    print(f"포트주소     :{test_con.port}")
    server_address = (myip, int(test_con.port))
    fail_counter = 0
    for i in range(counter):
        time.sleep(1)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect(server_address)
            sock.close()
            print(f"{i + 1} {test_con.container_name} Connection Succeed")
        except:
            print(f"{i + 1} {test_con.container_name} Connection Failed")
            fail_counter += 1
    sock.close()
    if fail_counter:
        return False
    else:
        return True


def get_setting_path():
    """
    find the setting.py's directory
    """
    setting_path = ""
    for path, dirs, files in os.walk(os.getcwd()):
        for i in files:
            if i == 'wsgi.py':
                setting_path = path
                break
    osType = get_sys()
    if osType == "Win":
        return setting_path.split("\\")[-1]
    else:
        return setting_path.split("/")[-1]


def revise_dockerfile(execute_file, requirements_path, deploydockerfile):
    """
    dockerfile의 test 를 실행 할 때 사용할 설정 파일을 수정해줍니다.
    Args:
        execute_file ([파일이름]])
    """
    global project_dir, docker_work_dir
    context = f"FROM python:3.10\nENV PYTHONUNBUFFERED 1\nWORKDIR {docker_work_dir}\nCOPY . .\n#deploy.py에서 requirements_path를 수정해주세요\n#다른 폴더에 있다면 폴더이름/텍스트파일.txt 의 형식입니다.\nRUN pip3 install -r {requirements_path}\nRUN pip3 install django\nRUN python3 {execute_file} test"
    f = open(f"{deploydockerfile}", 'w', encoding='UTF-8')
    f.write(context)
    f.close()


def shut_img_con(con, img):
    os.system(f"docker rm -f {con}")
    os.system(f"docker rmi -f {img}")
    # os.system(f"docker image prune -f")#


def fail_checker(cmd, con, img, deploylogfile, message):
    lines = cmd.split("\n")
    for i in lines:
        line = i.lower()
        f = open(f"{deploylogfile}", "a")
        f.write(line)
        f.write('\n')
        if "error" in line:
            shut_img_con(con, img)
            f.close()
            raise Exception(message)
    f.close()
    return True


def make_deploy_logs(deploylogfile):
    f = open(f"{deploylogfile}", "w")
    f.write("")
    f.close()


def env_getter():
    global project_dir_core
    f = open(f"{project_dir_core}/.env", "r", encoding="UTF-8")
    target = open(f"{Path(__file__).resolve().parent}/.env", "w", encoding="UTF-8")
    target.write(f.read())
    target.close()
    f.close()


def main():
    make_globals()
    try:
        env_getter()
    except:
        raise Exception(".env파일을 프로젝트 경로 위에 만들어 주세요")
    deploy()


if __name__ == "__main__":
    main()  #
