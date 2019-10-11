#!/usr/bin/python3

import os, sys, re, time,sys

try:
    import paramiko
except:
    import os

    os.system('pip3 install paramiko')
    import paramiko
bash_path = os.path.abspath(os.path.dirname(os.getcwd()))
sys.path.append(bash_path)


class set:
    def __init__(self, db, lb, nfs, rsync, web, zabbix):
        self.db = db
        self.lb = lb
        self.nfs = nfs
        self.rsync = rsync
        self.web = web
        self.zabbix = zabbix



    def get_server(self, server):
        lis1 = []
        dic = {}
        for i in range(len(server)):
            if i == 0:
                pass
            else:
                key = '[%s0%s]' % (server[0], i)
                if isinstance(server[i], str):
                    dic[key] = server[i]
                else:
                    for j in range(len(server[i])):
                        lis1.append(server[i][j])
                    dic[key] = lis1
        return dic
        # print(dic) :  {'[db01]': '10.0.0.151', '[db02]': '10.0.0.152'}

    def ansible(self, path):
        server = [self.db, self.lb, self.nfs, self.rsync, self.web, self.zabbix]
        lis2 = []
        for i in range(len(server)):
            if len(server[i]) == 1:
                pass
            else:
                lis2.append(s.get_server(server[i]))

        f = open(path, mode='r', encoding="utf-8")
        lis = []
        for line in f:
            if re.findall(
                    r'^#|^\s|^\[|((25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d))',
                    line):
                pass
            else:
                lis.append(line)
        f1 = open('hosts2', mode='a', encoding="utf-8")
        for line in lis:
            f1.write(str(line))
        # print(lis2) [{'[db01]': '10.0.0.151', '[db02]': '10.0.0.152'}, {'[nfs01]': ['10.0.0.160', '10.0.0.151']},
        for i in range(len(lis2)):
            dic = list(lis2)[i]
            # print(dic) {'[db01]': '10.0.0.151', '[db02]': '10.0.0.152'}
            for key in dic:
                f1.write(key)
                f1.write('\n')
                if isinstance(dic[key], str):
                    f1.write(str(dic[key]))
                    f1.write('\n')
                else:
                    for j in range(len(dic[key])):
                        f1.write(str(dic[key][j]))
                        f1.write('\n')
        f.close()
        f1.close()
        os.remove(path)
        os.rename('hosts2', path)

    def cheageip(self, file, dic, num=1):

        f = open(file, mode='r', encoding="utf-8")
        f1 = open('tmp', mode='a', encoding="utf-8")
        lis = []
        for key in dic:
            lis.append(dic[key])
        # print(lis[0])
        res0 = 0
        i = 0
        for line in f:
            if line and res0 == 0 and i < len(lis):
                res = re.subn(
                    r'(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)',
                    lis[i], line, 1)
                f1.write(str(res[0]))
                res0 = res[1]
                if res[1] and num - 1 == 0:
                    i = i + 1
            else:
                res0 = 0
                f1.write(str(line))

        f.close()
        f1.close()
        os.remove(file)
        os.rename('tmp', file)
        pass

    def mysql(self, path):
        app1 = path + 'app1.cnf'
        # atlas = path + 'test.cnf'
        dic = s.get_server(self.db)
        s.cheageip(app1, dic)
        # s.cheageip(atlas, dic)
        pass

    def nfs_(self, path, net):
        expor = path + 'exports'
        confxml = path + 'confxml.xml'
        dic = {'net': net[1]}
        s.cheageip(expor, dic)
        dic1 = s.get_server(self.rsync)
        s.cheageip(confxml, dic1)
        pass

    def web01(self, path):
        database = path + 'database.php'
        wp = path + 'wp-config.php'

        dicdb = s.get_server(self.db)

        s.cheageip(database, dicdb)
        s.cheageip(wp, dicdb)

    def zabbix01(self, path):
        zabbix_conf = path + 'zabbix.conf.php'
        zabbix_server = path + 'zabbix_server.conf'
        dicdb = s.get_server(self.db)
        s.cheageip(zabbix_conf, dicdb)
        s.cheageip(zabbix_server, dicdb)

    def get_all_ip(self, path):
        self.allip = []

        def get_ip(lis):
            for dic in lis:
                for key in dic:
                    lis_ip = [key[1:-1], dic[key]]
                    self.allip.append(lis_ip)
                    f1.write(str(dic[key]))
                    f1.write('\n')

        ip_txt = path
        server = [self.db, self.lb, self.nfs, self.rsync, self.web, self.zabbix]
        lis = []
        for i in range(len(server)):
            if len(server[i]) == 1:
                pass
            else:
                lis.append(s.get_server(server[i]))
        f1 = open('tmp', mode='a', encoding="utf-8")
        get_ip(lis)
        f1.close()
        try:
            os.remove(ip_txt)
        except Exception:
            pass
        os.rename('tmp', ip_txt)

    # def yaml_(self, path):
    #     ip_txt = path + 'ip.txt'
    #     fst = path + 'web01.yaml'
    #     main_yaml = path + 'main.yaml'
    #     dicfst = s.get_server(self.nfs)
    #
    #     s.get_all_ip(ip_txt)
    #     s.cheageip(fst, dicfst, num=2)
    #
    #     f2 = open('tmp', mode='a', encoding="utf-8")
    #     server = [self.db, self.lb, self.nfs, self.rsync, self.web, self.zabbix]
    #     for i in range(len(server)):
    #         for j in range(len(server[i])):
    #             if j >= 1:
    #                 ser = server[i][0]+'0'+str(j)
    #                 f2.write('- import_playbook: %s.yaml' % ser)
    #                 f2.write('\n')
    #
    #     f2.close()
    #     os.remove(main_yaml)
    #     os.rename('tmp', main_yaml)
    #     # - import_playbook: db01.yaml
    #     # - import_playbook: db02.yaml
    #     # - import_playbook: lb01.yaml
    #     # - import_playbook: lb02.yaml
    #     # - import_playbook: nfs01.yaml
    #     # - import_playbook: rsync01.yaml
    #     # - import_playbook: web01.yaml
    #     # - import_playbook: web03.yaml
    #     # - import_playbook: db03.yaml
    #     # - import_playbook: zabbix01.yaml
    def yaml_shell(self, path):
        ip_txt = 'yaml/ip.txt'
        s.get_all_ip(ip_txt)

        fst = path + 'web01.yaml'
        build_path = 'yaml.sh'
        dicfst = s.get_server(self.nfs)
        s.cheageip(fst, dicfst, num=2)

        f2 = open('tmp', mode='a', encoding="gbk")
        server = [self.db, self.lb, self.nfs, self.rsync, self.web, self.zabbix]
        f2.write('#!/bin/bash\n\ncase $1 in\n')

        for i in range(len(server)):
            for j in range(len(server[i])):
                if j >= 1:
                    ser = server[i][0] + '0' + str(j)
                    f2.write('%s)\nansible-playbook yaml/%s.yaml\n;;\n' % (ser, ser))
        f2.write('*)\necho "not thing to do!"\n;;\nesac\n')
        f2.close()
        try:
            os.remove(build_path)
        except Exception:
            pass
        os.rename('tmp', build_path)

    def hostname(self):
        # print(self.allip) [['db01', '10.0.0.171'], ['lb01', '10.0.0.172'], ['nfs01', '10.0.0.173'], ['rsync01', '10.0.0.174'], ['web01', '10.0.0.175'], ['zabbix01', '10.0.0.170']]
        try:
            for ip in self.allip:
                try:
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(hostname=ip[1], username='root', password='1')
                    client.exec_command('hostnamectl set-hostname %s' % ip[0])
                    print('%s set-hostname %s successful' % (ip[1], ip[0]))
                    client.close()
                except Exception as err:
                    print('%s set-hostname %s false' % (ip[1], ip[0]))
            return True
        except Exception as err:
            return False

    def test(self):
        ip_txt = 'yaml/ip.txt'
        s.get_all_ip(ip_txt)
        f = open('result', mode='a', encoding="utf-8")
        def get_result(server,ip):
            stdin, stdout, stderr = client.exec_command('systemctl status %s' % server)
            res = re.findall(r'active \(\w+\)', stdout.read().decode())
            res = res[0]
            print('The server %s in %s is %s' % (server, ip, res))
            if res == 'active (running)':
                return True
            else:

                f.write('The server %s in %s is %s\n' % (server, ip, res))

        servers = {'db': 'mysqld', 'lb': ['nginx', 'keepalived'], 'web': ['nginx', 'php-fpm,nfs'],
                   'nfs': ['nfs', 'rsyncd'],
                   'rsync': ['rpcbind', 'rsyncd'], 'zabbix': ['zabbix-agent', 'zabbix-server', 'httpd'], }
        try:
            for ip in self.allip:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=ip[1], username='root', password='1')
                servername = re.findall(r'\D+', ip[0])
                if len(servers[servername[0]]) > 1:
                    for num in range(len(servers[servername[0]])):
                        server = servers[servername[0]][num]
                        get_result(server,ip[1])

                else:
                    server = servers[servername]
                    get_result(server,ip[1])
                client.close()

        except Exception as err:
            print(err)
            return False
        f.close()

    def waiting(self):
        wait = True
        while wait:
            try:
                res = os.popen('cat /root/.jenkins/workspace/sushijie/tmp|wc -l').read()
                print(res,'in 7 job is finshed wait others for 120s')
                time.sleep(1)
                if res < 7:
                    time.sleep(120)
                else:
                    wait = False
            except Exception:
                pass

if __name__ == '__main__':
    net = ['net',
           '10.0.0.0']
    db = ['db',
          '10.0.0.168']
    lb = ['lb',
          ]
    nfs = ['nfs',
           '10.0.0.164']
    rsync = ['rsync',
             '10.0.0.105']
    web = ['web',
           '10.0.0.174']
    zabbix = ['zabbix',
              '10.0.0.170']
    ansible_path = '/etc/ansible/hosts'
    # ansible_path = 'hosts'
    mysql_path = 'mysql/conf/'
    nfs_path = 'nfs/conf/'
    web01_path = 'web01/conf/'
    zabbix_path = 'zabbix/conf/'
    yaml_path = 'yaml/'
    # try:
    s = set(db, lb, nfs, rsync, web, zabbix)
    if len(sys.argv) > 1 and hasattr(s, sys.argv[1]):
        getattr(s, sys.argv[1])()
        print('server %s done' % sys.argv[1])
    # if len(sys.argv) > 1 and sys.argv[1] == 'test':
    #     s.test()
    #     print('server test done')
    # elif len(sys.argv) > 1 and sys.argv[1] == 'wait':
    #     s.waiting()
    else:
        s.ansible(ansible_path)
        s.mysql(mysql_path)
        s.nfs_(nfs_path, net)
        s.web01(web01_path)
        s.zabbix01(zabbix_path)
        s.yaml_shell(yaml_path)
        if s.hostname():
            print('set-hostname successful')
        else:
            print('set-hostname false')

        print('All done')

