import winreg

def read_registry(key, value):
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as hkey:
            data, _ = winreg.QueryValueEx(hkey, value)
            return data
    except FileNotFoundError:
        return None
    except OSError as e:
        print(f"Ошибка доступа к реестру: {e}")
        return None

# Функция для чтения информации о пользователях
def get_user_info():
    user_info_list = []
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList') as hkey:
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(hkey, i)
                    subkey_path = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\{}'.format(subkey_name)
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path) as subkey:
                        profile_path = read_registry(subkey_path, 'ProfileImagePath')
                        user_info_list.append({
                            'Profile Path': profile_path
                        })
                    i += 1
                except OSError:
                    break
    except FileNotFoundError:
        pass
    except OSError:
        pass

    return user_info_list

# Функция для чтения информации о сетевых адаптерах
def get_network_stack_info():
    network_adapter_list = []
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces') as hkey:
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(hkey, i)
                    subkey_path = r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{}'.format(subkey_name)
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path) as subkey:
                        adapter_name = read_registry(subkey_path, 'Description') or read_registry(subkey_path, 'AdapterName')
                        dhcp_enabled = read_registry(subkey_path, 'EnableDHCP')
                        ip_address = read_registry(subkey_path, 'DhcpIPAddress') or read_registry(subkey_path, 'IPAddress')
                        subnet_mask = read_registry(subkey_path, 'DhcpSubnetMask') or read_registry(subkey_path, 'SubnetMask')
                        network_adapter_list.append({
                            'Adapter Name': adapter_name,
                            'DHCP Enabled': dhcp_enabled,
                            'IP Address': ip_address,
                            'Subnet Mask': subnet_mask
                        })
                    i += 1
                except OSError:
                    break
    except FileNotFoundError:
        pass
    except OSError:
        pass

    return network_adapter_list

# Функция для чтения информации об операционной системе
def get_os_info():
    os_name = read_registry(r'SOFTWARE\Microsoft\Windows NT\CurrentVersion', 'ProductName')
    os_version = read_registry(r'SOFTWARE\Microsoft\Windows NT\CurrentVersion', 'DisplayVersion')
    os_install_date = read_registry(r'SOFTWARE\Microsoft\Windows NT\CurrentVersion', 'InstallDate')
    return {
        'Name': os_name,
        'Version': os_version,
        'Install Date': os_install_date
    }

# Функция для чтения информации о процессоре и видеокарте
def get_cpu_info():
    cpu_name = read_registry(r'HARDWARE\DESCRIPTION\System\CentralProcessor\0', 'ProcessorNameString')
    cpu_Identifier = read_registry(r'HARDWARE\DESCRIPTION\System\CentralProcessor\0', 'Identifier')
    video_card = read_registry(r'SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000', 'DriverDesc')
    return {
        'CPU_NAME': cpu_name,
        'CPU_Identifier': cpu_Identifier,
        'Video_card': video_card
    }

# Функция для чтения информации о BIOS
def get_bios_info():
    bios_manufacturer = read_registry(r'HARDWARE\DESCRIPTION\System\BIOS', 'SystemManufacturer')
    bios_Family = read_registry(r'HARDWARE\DESCRIPTION\System\BIOS', 'SystemProductName')
    bios_version =  read_registry(r'HARDWARE\DESCRIPTION\System\BIOS', 'BIOSVersion')
    bios_vendor = read_registry(r'HARDWARE\DESCRIPTION\System\BIOS', 'BIOSVendor')
    return {
        'BIOS_Manufacturer': bios_manufacturer,
        'BIOS_Family': bios_Family,
        'BIOS_Version': bios_version,
        'BIOS_Vendor': bios_vendor
    }

# Функция для чтения информации об установленном программном обеспечении
def get_software_info():
    software_list = []
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall') as hkey:
            i = 0
            while True:
                subkey_name = winreg.EnumKey(hkey, i)
                subkey_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{}'.format(subkey_name)
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path) as subkey:
                    display_name = read_registry(subkey_path, 'DisplayName')
                    install_date = read_registry(subkey_path, 'InstallDate')
                    software_list.append({
                        'Display Name': display_name,
                        'Install Date': install_date
                    })
                i += 1
    except FileNotFoundError:
        pass
    except OSError:
        pass

    return software_list

# Функция для чтения информации о времени
def get_time_info_from_registry():
    time_info = {}

    try:
        time_zone = read_registry(r'SYSTEM\CurrentControlSet\Control\TimeZoneInformation', 'TimeZoneKeyName')
        time_info['Time Zone'] = time_zone
    except FileNotFoundError:
        pass
    except OSError:
        pass

    return time_info

# Основная функция для вывода информации на экран
def print_section(title):
    print(f"\n{'='*40}\n{title}\n{'='*40}\n")

def main():
    print('1 - Вся информация о пользователях')
    print('2 - Вся информация о сети')
    print('3 - Вся информация об операционной системе')
    print('4 - Вся информация об оборудовании')
    print('5 - Вся информация о BIOS')
    print('6 - Информация о программном обеспечении')
    print('7 - Информация о часовом поясе')
    n = int(input('Введите число - '))
    if n == 1:
        user_info = get_user_info()
        print_section('Информация о пользователях:')
        for user in user_info:
            for key, value in user.items():
                print(f'{key}: {value}')
            print('-' * 40)
    elif n == 2:
        network_stack_info = get_network_stack_info()
        print_section('Информация о сетевом стеке:')
        for adapter in network_stack_info:
            for key, value in adapter.items():
                print(f'{key}: {value}')
            print('-' * 40)
    elif n == 3:
        os_info = get_os_info()
        print_section('Информация об операционной системе:')
        for key, value in os_info.items():
            print(f'{key}: {value}')
    elif n == 4:
        cpu_info = get_cpu_info()
        print_section('Информация об оборудовании:')
        for key, value in cpu_info.items():
            print(f'{key}: {value}')
    elif n == 5:
        bios_info = get_bios_info()
        print_section('Информация о BIOS:')
        for key, value in bios_info.items():
            print(f'{key}: {value}')
    elif n == 6:
        software_info = get_software_info()
        print_section('Информация о программном обеспечении:')
        for software in software_info:
            for key, value in software.items():
                print(f'{key}: {value}')
            print('-' * 40)
    elif n == 7:
        time_info = get_time_info_from_registry()
        print_section('Информация о времени:')
        for key, value in time_info.items():
            print(f'{key}: {value}')

if __name__ == '__main__':
    main()
