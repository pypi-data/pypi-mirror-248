# coding=utf-8
import shutil
import re
import os
import sys
import time
import json
import platform
import tempfile
import traceback

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) > 1:
                shutil.copy2(s, d)

def extractall(self, path=None, members=None, pwd=None):
    if members is None: members = self.namelist()
    path = os.getcwd() if path is None else os.fspath(path)
    for zipinfo in members:
        try:    _zipinfo = zipinfo.encode('cp437').decode('gbk')
        except: _zipinfo = zipinfo.encode('utf-8').decode('utf-8')
        print('[*] unpack...', _zipinfo)
        if _zipinfo.endswith('/') or _zipinfo.endswith('\\'):
            myp = os.path.join(path, _zipinfo)
            if not os.path.isdir(myp):
                os.makedirs(myp)
        else:
            myp = os.path.join(path, _zipinfo)
            youp = os.path.join(path, zipinfo)
            self.extract(zipinfo, path)
            if myp != youp:
                os.rename(youp, myp)
import zipfile
zipfile.ZipFile.extractall = extractall

def creat_windows_shortcut(exe_path, name=None):
    vbsscript = '\n'.join([
        'set WshShell = WScript.CreateObject("WScript.Shell" )',
        'set oShellLink = WshShell.CreateShortcut(Wscript.Arguments.Named("shortcut") & ".lnk")',
        'oShellLink.TargetPath = Wscript.Arguments.Named("target")',
        'oShellLink.WindowStyle = 1',
        'oShellLink.Save',
    ])
    s = tempfile.mkdtemp()
    try:
        vbs = os.path.join(s, 'temp.vbs')
        with open(vbs, 'w', encoding='utf-8') as f:
            f.write(vbsscript)
        exe  = exe_path
        link = os.path.join(os.path.expanduser("~"), 'Desktop', name or os.path.split(exe_path)[1])
        if os.path.isfile(link + '.lnk'):
            os.remove(link + '.lnk')
        cmd = r'''
        {} /target:"{}" /shortcut:"{}"
        '''.format(vbs, exe, link).strip()
        print('[*] make shortcut in Desktop:', cmd)
        v = os.popen(cmd)
        v.read()
        v.close()
    finally:
        if traceback.format_exc().strip() != 'NoneType: None':
            print('create shortcut failed.')
            traceback.print_exc()
        shutil.rmtree(s)

# zip_path_exe
def get_zip_path_exe(zip, path, exe):
    localpath = os.path.split(__file__)[0]
    v_tools_file = os.path.join(localpath, zip)
    if '/' in path:
        path, inner  = path.split('/')
        v_tools_target = os.path.join(os.path.split(sys.executable)[0], 'Scripts', path)
        v_tools_exec = os.path.join(v_tools_target, inner, exe)
    else:
        v_tools_target = os.path.join(os.path.split(sys.executable)[0], 'Scripts', path)
        v_tools_exec = os.path.join(v_tools_target, exe)
    return {
        'file': v_tools_file,
        'target': v_tools_target,
        'exec': v_tools_exec,
        'type': 'zip_path_exe',
        'path': path,
        'exe': exe,
    }
# zip_path_exe
def unpack_v_zip_path_exe(zeobj):
    print('[*] zip file path ===>', zeobj['file'])
    print('[*] exe file path ===>', zeobj['exec'])
    if not os.path.isdir(zeobj['target']):
        print('[*] unpack...')
        f = zipfile.ZipFile(zeobj['file'], 'r')
        f.extractall(zeobj['target'])
        f.close()
        print('[*] unpacked path ===>', zeobj['target'])
    creat_windows_shortcut(zeobj['exec'], zeobj['exe'])
# zip_path_exe
def remove_v_zip_path_exe(zeobj, kill_process=True):
    if os.path.isdir(zeobj['target']):
        if kill_process:
            os.popen('taskkill /f /im "{}" /t'.format(zeobj['exe'])).read()
        print('[*] remove...', zeobj['target'])
        time.sleep(0.2)
        for i in range(10):
            try:
                shutil.rmtree(zeobj['target'])
                break
            except:
                print('[*] wait...')
                time.sleep(0.2)
        link = os.path.join(os.path.expanduser("~"), 'Desktop', zeobj['exe'])
        if os.path.isfile(link + '.lnk'):
            os.remove(link + '.lnk')

def get_scripts_scrt_desktop(zip, path, password_tips):
    localpath = os.path.split(__file__)[0]
    v_tools_file = os.path.join(localpath, zip)
    v_tools_target = os.path.join(os.path.expanduser("~"), 'Desktop', path)
    return {
        'file': v_tools_file,
        'target': v_tools_target,
        'password_tips': password_tips,
    }
# zip_path_exe
def unpack_v_scripts_scrt_desktop(zeobj):
    if zeobj['password_tips'] == 'none':
        if not os.path.isdir(zeobj['target']):
            print('[*] unpack...')
            f = zipfile.ZipFile(zeobj['file'], 'r')
            f.extractall(zeobj['target'])
            f.close()
            print('[*] unpacked path ===>', zeobj['target'])
    else:
        print('[*] zip file path ===>', zeobj['file'])
        if not os.path.isdir(zeobj['target']):
            os.makedirs(zeobj['target'])
        shutil.copy(zeobj['file'], zeobj['target'])
        print('[*] unpacked path ===>', zeobj['target'])
        print('[*] password_tips:', zeobj['password_tips'])

# zip_path_exe
def remove_v_scripts_scrt_desktop(zeobj):
    if os.path.isdir(zeobj['target']):
        print('[*] remove...', zeobj['target'])
        time.sleep(0.2)
        for i in range(10):
            try:
                shutil.rmtree(zeobj['target'])
                break
            except:
                print('[*] wait...')
                time.sleep(0.2)

def install_tcc():
    if platform.architecture()[0].startswith('32'):
        _ver = '32'
    elif platform.architecture()[0].startswith('64'):
        _ver = '64'
    curr = os.path.dirname(__file__)
    targ = os.path.join(os.path.dirname(sys.executable), 'Scripts')
    _tcc = 'tcc-0.9.27-win{}-bin.zip'.format(_ver)
    if os.path.isfile(os.path.join(targ, 'tcc.exe')):
        print('[*] tcc is installed.')
        return
    print('init tcc tool: {}'.format(_tcc))
    tcc = os.path.join(curr, _tcc)
    zf = zipfile.ZipFile(tcc)
    zf.extractall(path = targ)
    winapi = os.path.join(curr, 'winapi-full-for-0.9.27.zip')
    zf = zipfile.ZipFile(winapi)
    zf.extractall(path = targ)
    fd = 'winapi-full-for-0.9.27'
    finclude = os.path.join(targ, fd, 'include')
    tinclude = os.path.join(targ, 'tcc', 'include')
    copytree(finclude, tinclude)
    shutil.rmtree(os.path.join(targ, fd))
    tccenv = os.path.join(targ, 'tcc')
    copytree(tccenv, targ)
    print('tcc in {}'.format(targ))
    shutil.rmtree(tccenv)

install_list = [
    {
        'name': 'sublime',
        'type': 'zip_path_exe',
        'info': ['sublime3.zip', 'sublime3', 'sublime_fix.exe']
    },
    {
        'name': 'scrcpy',
        'type': 'zip_path_exe',
        'info': ['scrcpy-win64-v2.1.1.zip', 'scrcpy/scrcpy-win64-v2.1.1', 'scrcpy.exe']
    },
    # {
    #     'name': 'VC_redist.x64',
    #     'type': 'scripts_scrt_desktop',
    #     'info': ['VC_redist.x64.zip', 'VC_redist.x64', 'none']
    # },
    {
        'name': 'tcc',
        'type': 'tcc',
    },
]

def install(name=None):
    for meta in install_list:
        if (not name) or (name and meta['name'] == name):
            if meta['type'] == 'tcc':
                install_tcc()
            if meta['type'] == 'zip_path_exe':
                unpack_v_zip_path_exe(get_zip_path_exe(meta['info'][0], meta['info'][1], meta['info'][2]))
            if meta['type'] == 'scripts_scrt_desktop':
                unpack_v_scripts_scrt_desktop(get_scripts_scrt_desktop(meta['info'][0], meta['info'][1], meta['info'][2]))

def remove(name=None, kill_process=True):
    for meta in install_list:
        if (not name) or (name and meta['name'] == name):
            if meta['type'] == 'zip_path_exe':
                remove_v_zip_path_exe(get_zip_path_exe(meta['info'][0], meta['info'][1], meta['info'][2]), kill_process)
            if meta['type'] == 'scripts_scrt_desktop':
                remove_v_scripts_scrt_desktop(get_scripts_scrt_desktop(meta['info'][0], meta['info'][1], meta['info'][2]))

def execute():
    argv = sys.argv
    print('v_tools :::: [ {} ]'.format(' '.join(argv)))
    if len(argv) == 1:
        print('[install]:  v_tools install')
        print('[remove]:   v_tools remove')
        for installer in install_list:
            print('[tool]:', installer['name'])
        return
    if len(argv) > 1:
        if argv[1] == 'install':
            if len(argv) > 2:
                install(argv[2])
            else:
                install()
        if argv[1] == 'remove':
            if len(argv) > 2:
                remove(argv[2])
            else:
                remove()

def readfilecode(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()

def readfilebyte(file):
    with open(file, 'rb') as f:
        return f.read()


def _make_bit_dll_file(file, bit='64'):
    file_path = os.path.split(file)[0]
    tempfile_cname = 'v_temp_file.c'
    tempfile_dllname = 'v_temp_dll.dll'
    tempfilec = '{}/{}'.format(file_path, tempfile_cname)
    tempfiledll = '{}/{}'.format(file_path, tempfile_dllname)
    ccode = readfilecode(file)
    inject_config = re.findall('inject((?: +"[^ ]*")*)', ccode.strip().splitlines()[0])
    combine_expr = r'// *=* *before is dll *=* *[^\n]+\n'
    dll_ccode = re.split(combine_expr, ccode)[0]
    is_combine_file = bool(re.findall(combine_expr, ccode))
    combine_file_code = re.split(combine_expr, ccode)[1] if is_combine_file else None
    if not inject_config:
        print('[*] not find inject config in cfile 1.')
        return
    if inject_config:
        inject_config = re.split(' +', inject_config[0].strip())
        if not inject_config:
            print('[*] not find inject config in cfile 2.')
            return
        for idx,_ in enumerate(inject_config):
            inject_config[idx] = inject_config[idx].strip('"').strip("'")
        python_exe_path = sys.executable
        try:
            with open(tempfilec, 'w', encoding='utf-8') as f:
                f.write(dll_ccode)
            if bit == '32':
                os.system('tcc -m32 -shared "{}" -o "{}"'.format(tempfilec, tempfiledll))
            if bit == '64':
                os.system('tcc -m64 -shared "{}" -o "{}"'.format(tempfilec, tempfiledll))
            content = readfilebyte("{}/{}.dll".format(file_path, 'v_temp_dll'))
            ret = ''
            for i in content:
                ret += str(i)+','
            dllcode = '{' + ret[:-1] + '}'
            enumbyname = None
            findbyname = None
            if len(inject_config) == 1:
                enumbyname = 'v_EnumProcessByName("{}");'.format(inject_config[0])
                findbyname = 'HANDLE proc = v_FindProcessByName("{}");'.format(inject_config[0])
            if len(inject_config) == 2:
                enumbyname = 'v_EnumProcessByNameAndCommand("{}", L"{}");'.format(inject_config[0], inject_config[1])
                findbyname = 'HANDLE proc = v_FindProcessByNameAndCommand("{}", L"{}");'.format(inject_config[0], inject_config[1])
            if len(inject_config) == 3:
                enumbyname = 'v_EnumProcessByNameAndPosRevCommand("{}", L"{}", L"{}");'.format(inject_config[0], inject_config[1], inject_config[2])
                findbyname = 'HANDLE proc = v_FindProcessByNameAndPosRevCommand("{}", L"{}", L"{}");'.format(inject_config[0], inject_config[1], inject_config[2])
            repcode = '''
    unsigned char DLLBit[] = '''+dllcode+''';
    LPVOID base = (char*)DLLBit;
    '''+enumbyname+'''
    '''+findbyname+'''
    printf("[*] proc: %d\\n", proc);
    v_InjectDllRef(base, proc);
'''
            return [is_combine_file, repcode, combine_file_code]
        except:
            traceback.print_exc()
        finally:
            if os.path.isfile(tempfilec): 
                os.remove(tempfilec)
            if os.path.isfile(tempfiledll): 
                os.remove(tempfiledll)

def inject(file, bit='64'):
    dll_repcode = _make_bit_dll_file(file, bit)
    if not dll_repcode:
        print('[*] not a dll inject dll.')
        ccode = readfilecode(file)
        shared = ''
        if ' DllMain(' in ccode:
            shared = '-shared'
        if file.endswith('.c'):
            if bit == '32':
                cmd = 'tcc -m32 {} "{}"'.format(shared, file)
            if bit == '64':
                cmd = 'tcc -m64 {} "{}"'.format(shared, file)
            print('[*] run cmd: {}'.format(cmd))
            os.system(cmd)
        if shared:
            exefile = 'regsvr32.exe /s "{}"'.format(file.rsplit('.', 1)[0] + '.dll')
        else:
            exefile = '"{}"'.format(file.rsplit('.', 1)[0] + '.exe')
        try:
            print('[*] run file: {}'.format(exefile))
            os.system(exefile)
        except:
            print(traceback.format_exc())
        return

    is_combine_file, repcode, combine_file_code = dll_repcode
    python_exe_path = sys.executable
    file_path = os.path.split(file)[0]
    tempfilec = '{}/{}.c'.format(file_path, 'v_temp_mk_c')

    exefile = None
    def make_exe(rscript):
        with open(tempfilec, 'w', encoding='utf-8') as f:
            f.write(rscript)
        print('[*] write in file:{}'.format(tempfilec))
        filename = os.path.split(file)[1]
        if '.' in filename:
            filename = filename.rsplit('.', 1)[0]
        if bit == '32':
            cmd = 'tcc -m32 "{}" -o "{}/{}.exe"'.format(tempfilec, file_path, filename)
        if bit == '64':
            cmd = 'tcc -m64 "{}" -o "{}/{}.exe"'.format(tempfilec, file_path, filename)
        print('[*] run cmd: {}'.format(cmd))
        os.system(cmd)
        return '"{}/{}.exe"'.format(file_path, filename)
    try:
        if not is_combine_file:
            print('[*] is_combine_file:', is_combine_file)
            DllDev = os.path.join(os.path.split(python_exe_path)[0], 'Scripts/sublime3/Data/Packages/User/v_snippet/tcc_dll_inject.sublime-snippet')
            if not os.path.isfile(DllDev):
                print('v_tools sublime not install.')
                return
            dcode = readfilecode(DllDev)
            cscript = re.findall(r'<!\[CDATA\[([\s\S]*)\]\]>', dcode)[0]
            intmain = re.findall(r'((int main[^\{]+\{)[\s\S]*(\}[ \r\n]*))$', cscript)[0]
            rscript = cscript.replace(intmain[0], intmain[1] + repcode + intmain[2])
        else:
            print('[*] is_combine_file:', is_combine_file)
            rscript = combine_file_code.replace('printf("@inject");', repcode).replace('// @inject', repcode)
        exefile = make_exe(rscript)
    except:
        print(traceback.format_exc())
    finally:
        if os.path.isfile(tempfilec): 
            os.remove(tempfilec)
    if exefile:
        try:
            print('[*] run file: {}'.format(exefile))
            os.system(exefile)
        except:
            print(traceback.format_exc())

def make_dll_inject_32():
    argv = sys.argv
    print('make_dll_inject_32 :::: [ {} ]'.format(' '.join(argv)))
    if len(argv) == 1:
        print('[*] first file must be a dll.c file.')
    if len(argv) > 1:
        file = argv[1]
        inject(file, '32')

def make_dll_inject_64():
    argv = sys.argv
    print('make_dll_inject_64 :::: [ {} ]'.format(' '.join(argv)))
    if len(argv) == 1:
        print('[*] first file must be a dll.c file.')
    if len(argv) > 1:
        file = argv[1]
        inject(file, '64')


def __setup():
    from setuptools import setup
    setup(
        # pip install twine
        # python setup.py bdist_wheel && twine upload dist/*
        # twine upload dist/*
        name = "vvv_tools",
        version = "0.1.2",
        packages = ["vvv_tools"],
        entry_points={
            'console_scripts': [
                'v_tools = vvv_tools:execute',
                'v_make_dll_inject_32 = vvv_tools:make_dll_inject_32',
                'v_make_dll_inject_64 = vvv_tools:make_dll_inject_64'
            ]
        },
        package_data ={
            "vvv_tools":[
                '*.zip',
            ]
        },
    )

if __name__ == '__main__':
    # execute()
    # install('tcc')
    # remove('sublime')

    testc = os.path.join(os.path.expanduser("~"),'Desktop','test.c')
    # _make_bit_dll_file(testc)
    inject(testc)

    pass
