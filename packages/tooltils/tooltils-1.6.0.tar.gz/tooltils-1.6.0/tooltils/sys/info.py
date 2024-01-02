"""Identifying system information"""

class _bm:
    from subprocess import CalledProcessError, TimeoutExpired, run
    from sys import executable, maxsize, platform, version
    from socket import gethostname
    from logging import getLogger

    def check(cmd: str, shell: bool=False):
        return _bm.run(cmd, shell=shell, capture_output=True).stdout.decode().splitlines()
    
    logger = getLogger('tooltils.sys.info')

macOS_releases: dict[str, str] = {
    "10.0":  "Cheetah",
    "10.1":  "Puma",
    "10.2":  "Jaguar",
    "10.3":  "Panther",
    "10.4":  "Tiger",
    "10.5":  "Leopard",
    "10.6":  "Snow Leopard",
    "10.7":  "Lion",
    "10.8":  "Mountain Lion",
    "10.9":  "Mavericks",
    "10.10": "Yosemite",
    "10.11": "El Capitan",
    "10.12": "Sierra",
    "10.13": "High Sierra",
    "10.14": "Mojave",
    "10.15": "Catalina",
    "11":    "Big Sur",
    "12":    "Monterey",
    "13":    "Ventura",
    "14":    "Sonoma"
}
"""List of all current MacOS versions"""

python_version:         str = _bm.version.split('(')[0].strip()
"""Current Python interpreter version"""
name:                   str = _bm.gethostname()
"""The network name of computer"""
bitsize                     = 64 if (_bm.maxsize > 2 ** 32) else 32
"""The bit limit of the current Python interpreter"""
interpreter:            str = _bm.executable
"""Location of current Python interpreter"""

st = _bm.platform.startswith
if st('linux'):
    tplatform = tdplatform = 'Linux'
elif st('win'):
    tplatform = tdplatform = 'Windows'
elif st('cygwin'):
    tplatform, tdplatform = 'Windows', 'Cygwin'
elif st('msys'):
    tplatform, tdplatform = 'Windows', 'MSYS2'
elif st('darwin'):
    tplatform, tdplatform = 'MacOS', 'Darwin'
elif st('os2'):
    tplatform = tdplatform = 'OS2'
elif st('risc'):
    tplatform, tdplatform = 'Linux', 'RiscOS'
elif st('athe'):
    tplatform, tdplatform = 'Linux', 'AtheOS'
elif st('freebsd'):
    tplatform, tdplatform = 'BSD', 'FreeBSD'
elif st('openbsd'):
    tplatform, tdplatform = 'BSD', 'OpenBSD'
elif st('aix'):
    tplatform = tdplatform = 'AIX'
else:
    tplatform = tdplatform = None

platform:          str = tplatform
"""Name of current operating system"""
detailed_platform: str = tdplatform
"""Detailed name of current operating system"""

if platform.lower() == 'macos':
    tpver: list = [_bm.check(['sw_vers', '-productVersion'])[0]]

    if len(tpver[0].split('.')) > 1:
        if tpver[0][:2] in ('11', '12', '13', '14'):
            tpver.append(macOS_releases[tpver[0][:2]])
        else:
            tpver.append(macOS_releases['.'.join(tpver[0].split('.')[:2])])
    else:
        tpver.append(macOS_releases[tpver[0]])
    
    tarch:     str = _bm.check('arch')[0]
    tsysinfo: list = list(filter(None, _bm.check(['system_profiler', 'SPHardwareDataType'])))
    tmodel:    str = tsysinfo[2].split(': ')[1]
    tcpu:      str = tsysinfo[5].split(': ')[1]
    tcores:    int = int(tsysinfo[6].split(': ')[1].split(' (')[0])
    tram:      str = tsysinfo[7].split(': ')[1]
    if 'GB' in tram:
        tram: int = int(tram.split(' ')[0]) * 1024
    else:
        tram: int = int(tram.split(' ')[0])
    tmanufacturer:  str = 'Apple Inc.'
    tserial_number: str = tsysinfo[10].split(': ')[1]
    tboot_drive:    str = _bm.check(['bless', '--info', '--getBoot'])[0]

elif platform.lower() == 'windows':
    def wmic(*cmds: tuple) -> str:
        return [i.strip() for i in _bm.check('wmic ' + cmds[0] + ' get ' + cmds[1])][2]

    tcpu:           str = wmic('cpu', 'name')
    tcores:         str = wmic('cpu', 'NumberOfCores')
    tserial_number: str = wmic('bios', 'SerialNumber')
    tarch:          str = wmic('os', 'OSArchitecture').replace('Processor', '').strip()

    tsysinfo: list = list(filter(None, _bm.check('systeminfo')))

    tversion:      str = tsysinfo[2]
    tmanufacturer: str = tsysinfo[11]
    tmodel:        str = tsysinfo[12]
    tboot_drive:   str = tsysinfo[19]
    tram:          str = tsysinfo[23]

    for i in ['tversion', 'tmanufacturer', 'tmodel', 'tboot_drive', 'tram']:
        locals()[i] = locals()[i].split(': ')[1].strip()

    tpver:  str = tversion.split(' ')[0]
    tram:   int = int(tram.split(' ')[0].replace(',', ''))
    tpver: list = [tpver.split('.')[0], tpver]
    
elif platform.lower() == 'linux':
    tcpu:      str = _bm.check('lscpu | grep \'Model:\'', True)[0].split(':')[1].strip()
    tarch:     str = _bm.check('arch')[0]
    tsysinfo: list = _bm.check(['cat', '/etc/os-release'])
    tpver:    list = [tsysinfo[3].split('"')[1].split(' ')[0], tsysinfo[1].split('"')[1]]
    tmodel:    str = _bm.check(['cat', '/sys/devices/virtual/dmi/id/product_name'])[0]
    tcores:    int = _bm.check('lscpu | grep \'Core(s) per socket:\'', True)[0].split(':')[1].strip()
    tram:      int = round(int(_bm.check('cat /proc/meminfo | grep \'MemTotal:\'', True)[0].split(':')[1].strip().split(' ')[0]) / 1000)
    tmanufacturer:  str = _bm.check(['cat', '/sys/devices/virtual/dmi/id/sys_vendor'])[0]
    tserial_number: str = ''
    tboot_drive:    str = _bm.check('df /boot | grep -Eo \'/dev/[^ ]+\'', True)[0]

    _bm.logger.warn('serial_number variable could not be obtained successfully in tooltils.sys.info')

else:
    tcpu:   str = ''
    tarch:  str = ''
    tpver: list = []
    tmodel: str = ''
    tcores: int = 0
    tram:   int = 0
    tmanufacturer:  str = ''
    tserial_number: str = ''
    tboot_drive:    str = ''

cpu:                     str = str(tcpu)
"""Name of the currently in use cpu of your computer"""
arch:                    str = str(tarch)
"""Architecture of your computer"""
platform_version: tuple[str] = tuple([str(i) for i in tpver])
"""Version number and or name of current OS"""
model:                   str = str(tmodel)
"""The model or manufacturer of your computer"""
cores:                   int = int(tcores)
"""The amount of cores in your computer cpu"""
ram:                     int = int(tram)
"""The amount of ram in megabytes in your computer"""
manufacturer:            str = str(tmanufacturer)
"""The organisation or company that created your computer"""
serial_number:           str = str(tserial_number)
"""The identifiable code or tag string of your computer"""
boot_drive:              str = str(tboot_drive)
"""The location of the boot drive currently being used on your computer"""

for i in ('_bm', 'st', 'tcpu', 'tarch', 'tpver',
          'tplatform', 'tdplatform', 'tmodel',
          'tcores', 'tram', 'tserial_number',
          'tboot_drive', 'tmanufacturer', 
          'tsysinfo', 'wmic'):
    try:
        del globals()[i]
    except KeyError:
        continue
