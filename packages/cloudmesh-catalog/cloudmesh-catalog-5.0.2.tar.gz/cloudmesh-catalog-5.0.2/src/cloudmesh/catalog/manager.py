import os
import socket
import sys
import time
import psutil

from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import readfile
from cloudmesh.common.systeminfo import get_platform
from cloudmesh.common.util import writefile
from cloudmesh.common.util import yn_choice

class ServiceManager:
    """
    ServiceManager Class

    This class provides functionality for managing a service, such as starting, stopping, and checking its status.

    Methods:
        - __init__(name=None): Initializes the ServiceManager instance.
        - is_port_in_use(): Checks if the specified port is in use.
        - start(): Starts the service.
        - get_pid(): Gets the process ID (PID) of the service.
        - stop(pid=None): Stops the service.
        - status(): Checks the status of the service.
        - pid_exists(pid): Checks if the specified PID exists.
        - info(): Retrieves information about the service.

    Attributes:
        - name (str): The name of the service.
        - path (str): The path to the service directory.
        - pid_file (str): The path to the PID file.
        - port (int): The port on which the service runs.
        - reload (str): The reload option for uvicorn.
    """

    # r = cloudmesh.common.SHell.run("uvicorn .... ")

    def __init__(self, name=None):
        """
         Initializes the ServiceManager instance.

         Args:
             name (str): The name of the service.

         Returns:
             None
         """
        self.name = name or "cloudmesh-catalog-service"
        self.path = path_expand("~/.cloudmesh/catalog")
        if get_platform() == "windows":
            self.path=self.path.replace("\\","/")
        self.pid_file = f"{self.path}/{self.name}.pid"
        self.port = 8001
        self.reload = "--reload"

        Shell.mkdir(self.path)

    def is_port_in_use(self) -> bool:
        """
        Checks if the specified port is in use.

        Returns:
            bool: True if the port is in use, False otherwise.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', self.port)) == 0

    def start(self):
        """
        Starts the service.

        Raises:
            RuntimeError: If the catalog server could not be started due to an error.

        Returns:
            None
        """

        name = f"{self.path}/{self.name}"
        try:
            os.system(f"rm -f {name}.pid")
        except:
            pass

        command = f"nohup uvicorn cloudmesh.catalog.service:app --port={self.port} {self.reload} " \
                  f"> {name}.log 2>&1 & echo $! > {name}.pid"

        if get_platform() == "windows":

            Console.error("The windows program has a bug when stopping the catalog. "
                          "At this time we stop all python and uvicorn processes")
            print()
            command = f"start //b uvicorn cloudmesh.catalog.service:app --port={self.port} {self.reload} " \
                      f"; bash"

            command = command.replace("\\", "/")
            print(command)
            pid = Shell.terminal(command=command)
            result = 0
            writefile(f"{name}.pid", str(pid))
        else:
            print(command)
            result = os.system(command)

        time.sleep(1)
        print(result)
        if result != 0:
            Console.error("The catalog server could not be started due to an error")
        try:
            content = readfile(f"{self.pid_file}")
            if "Address already in use" in content:
                Console.error("Address already in use")
            else:
                print(content)
        except:
            Console.error("pid file could not be found")

    def get_pid(self):
        """
        Gets the process ID (PID) of the service.

        Returns:
            str: The process ID (PID) of the service.
        """
        try:
            pid = readfile(f"{self.pid_file}").strip()
            # if not psutil.pid_exists(pid):
            #    pid = None
        except:
            pid = None
        return pid

    def stop(self, pid=None):
        """
        Stops the service.

        Args:
            pid (str): The process ID (PID) of the service. If None, the PID is retrieved from the service.

        Returns:
            None
        """
        if pid is None:
            info = self.info()
            pid = info["pid"]
        if get_platform() == 'windows':
            try:
                Console.error("The code has currently a bug and we delete simply all pyton and uviconr processes")
                if yn_choice("Would you like to delete them"):
                    print(f"Deleting all python and uvicorn processes ")

                    #
                    # this has another bug, as we run python we can not delete ourselfs
                    # find pids of all python.exe, and delete all but for this process
                    #
                    for command in ["uvicorn.exe", "python.exe"]:
                        try:
                            os.system(f"taskkill /f /IM {command}")
                        except:
                            pass
                    print ("ok.")
                    print(f"Deleting {pid} ", end="")
                    os.system(f"taskkill /f /t /pid {pid}")
                    print()
                    print("Please now kill the window by hand.")
                else:
                    return

            except Exception as e:
                r=None
                print(e)
        else:
            for child in psutil.Process(pid).children():
                try:
                    print(f"Deleting {child.pid} ", end="")
                    p = psutil.Process(child.pid)
                    p.kill()
                    Console.green("deleted.")

                except psutil.Error:
                    Console.red(". failed")

            print(f"Deleting {pid} ", end="")

            p = psutil.Process(pid)
            p.kill()
        Console.green("deleted.")
        try:
            Shell.rm(self.pid_file)
        except:
            Console.warning(f"Pid file already deleted.")


    def status(self):
        """
        Checks the status of the service.

        Returns:
            bool: True if the service is running, False otherwise.
        """
        # for debug only
        probe = Shell.run(f"curl localhost:{self.port}")
        return '{"Cloudmesh Catalog":"running"}' in probe

    def pid_exists(self, pid):
        """
        Checks if the specified PID exists.

        Args:
            pid (str): The process ID (PID) to check.

        Returns:
            bool: True if the PID exists, False otherwise.
        """
        if pid is None:
            return False
        r = Shell.run(f"ps {pid}").strip().splitlines()
        return len(r) > 1


    def info(self):
        """
        Retrieves information about the service.

        Returns:
            dotdict: A dotdict containing information about the service, including PID, status, port, and children.
        """

        data = dotdict({
            "pid": None,
            "children": None,
            "status": False,
            "port": self.port
        })
        try:
            data.pid = int(self.get_pid())
            if self.pid_exists(data.pid):
                Console.ok(f"The process with pid {data.pid} exists")
            else:
                Console.error(f"The process with pid does not {data.pid} exists")
                try:
                    Console.warning(f"Removing PID file: {self.pid_file}")
                    os.remove(self.pid_file)
                except:
                    pass
        except:
            pass
        try:
            data.status = self.status()
        except:
            pass
        try:
            data.children = [child.pid for child in psutil.Process(data.pid).children()]
        except Exception as e:
            pass

        return data
