# SD-WAN Device Initial Configuration Generator

## Description:

The [SD-WAN](https://www.cisco.com/c/en_ph/solutions/enterprise-networks/sd-wan/index.html) Device Initial Configuration Generator is a **Python** application that creates a text file which contains the initial configuration required for a Cisco SD-WAN device to be able to on-board to the SD-WAN network.

The application works by taking in multiple required and optional arguments from the user which it then uses to create an altered version of one of the input text files (depending on the device type argument specified). The altered version is saved as “output.txt” and rewritten every time the code is executed.

To view the source code, click [here](https://github.com/xMoAlaa7/SD-WAN-Initial-Configuration-Generator/blob/2de1cc55c4fdd676b7a6ef6710a24c0cf566f711/project.py) or to view a demo of the application, [here](https://youtu.be/YAkpe-EeDdY).

The application supports configuring the following devices:
- vSmart Controller
- vBond Orchestrator
- vManage Network Management System
- CSR1000v Edge Router (tested on version 16.12.4)

The application supports configuring the following parameters:
- Hostname
- System IP
- Site ID
- Organization Name
- vBond IP Address/Domain Name (Local on the vBond Orchestrator)
- Port Offset (This parameter is not supported for the vBond Orchestrator by nature of the device) (Optional)
- DNS (Optional)
- Local IP Address/Prefix
- Gateway IP Address

The application is dependent on the following text files which it reads from:
- [vsmart.txt](https://github.com/xMoAlaa7/SD-WAN-Initial-Configuration-Generator/blob/2de1cc55c4fdd676b7a6ef6710a24c0cf566f711/vsmart.txt)
- [vbond.txt](https://github.com/xMoAlaa7/SD-WAN-Initial-Configuration-Generator/blob/2de1cc55c4fdd676b7a6ef6710a24c0cf566f711/vbond.txt)
- [vmanage.txt](https://github.com/xMoAlaa7/SD-WAN-Initial-Configuration-Generator/blob/2de1cc55c4fdd676b7a6ef6710a24c0cf566f711/vmanage.txt)
- [csr.txt](https://github.com/xMoAlaa7/SD-WAN-Initial-Configuration-Generator/blob/2de1cc55c4fdd676b7a6ef6710a24c0cf566f711/csr.txt)

>[test_project.py](https://github.com/xMoAlaa7/SD-WAN-Initial-Configuration-Generator/blob/2de1cc55c4fdd676b7a6ef6710a24c0cf566f711/test_project.py) is code written to test the project's code using the [pytest](https://docs.pytest.org/en/7.4.x/) framework. It's supplied with commentary sufficient to allow the reader to understand what exactly is being tested.

## How it Works:

The application’s code includes 4 functions which the main function calls as follows:

```ruby
def main():
    configs = inputs()
    cleaner1(configs)
    configs_clean = cleaner2(configs)
    create_txt(configs_clean)
```

-	The inputs() function utilizes the [argparse](https://docs.python.org/3/library/argparse.html) library to take in the previously mentioned arguments from the user. It’s also configured to provide descriptions of each parameter and its limitations by invoking help.

```ruby
def inputs():
    parser = argparse.ArgumentParser(
        description=("Generate Cisco SD-WAN Initial Configuration")
    )
    parser.add_argument(
        "-t",
        help="Device Type: Can be vSmart, vManage, vBond, or CSR (case insensitive)",
    )
    parser.add_argument("-n", help="Hostname: Maximum characters is 32")
    parser.add_argument("-s", help="System IP")
    parser.add_argument("-i", help="Site ID: Maximum ID is 4294967295")
    parser.add_argument("-o", help="Organization Name: Maximum characters is 64")
    parser.add_argument("-v", help="vBond IP/Domain")
    parser.add_argument("-p", default="Skip", help="Port Offset: Ranges from 0 to 19")
    parser.add_argument("-d", default="Skip", help="DNS")
    parser.add_argument(
        "-l", help="Local IP: Prefix must be added at all times not the subnet mask."
    )
    parser.add_argument("-g", help="Gateway IP")
    args = parser.parse_args()
    return args
```

-	The cleaner1(args) function takes in the arguments namespace provided by the inputs() function and checks whether all the required parameters are inserted by the user or not.

```ruby
def cleaner1(args):
    l = [args.t, args.n, args.s, args.i, args.o, args.v, args.p, args.d, args.l, args.g]
    # Test if all required arguments were inserted by the user.
    print(l)
    for i in l:
        if i:
            continue
        else:
            sys.exit("Missing Arguments")
    return True
```

-	The cleaner2(args) function takes in the arguments namespace provided by the inputs() function, checks the device type specified, performs input-error checking on those arguments, and alters the Local IP Address depending on the device type parameter. This function returns a list of the input arguments in a specific order.

```ruby
def cleaner2(args):
    l = [args.t, args.n, args.s, args.i, args.o, args.v, args.p, args.d, args.l, args.g]
    try:
        # Test Device Type.
        match args.t.lower():
            case "vsmart" | "vbond" | "vmanage" | "csr":
                pass
            case _:
                sys.exit("Invalid Device Type")
        # Test Port Offset. Also returns ValueError if args.p isn't a string that is an integer.
        if args.p != "Skip":
            if 0 <= int(args.p) <= 19:
                if args.t.lower() == "vbond":
                    sys.exit("You cannot assign Port Offset to the vBond.")
                else:
                    pass
            else:
                sys.exit("Invalid Port Offset Range")
        # Test Site ID, Hostname, and Organization Name. Also returns ValueError if args.i isn't a string that is an integer.
        if (
            1 <= int(args.i) <= 4294967295
            and 1 <= len(args.n) <= 32
            and 1 <= len(args.o) <= 64
        ):
            pass
        else:
            sys.exit("Invalid Site ID, Hostname, or Organization Name")
        # Test vBond IP/Domain
        try:
            ipaddress.ip_address(args.v)
        except ValueError:
            print(
                "Alert: vBond parameter is assigned as a Domain Name so make sure it's correct. If you assigned an IP address and this message appears, the IP Address is incorrect."
            )
        # Test Local IP:
        locip = ipaddress.IPv4Interface(args.l)
        if args.t.lower() == "csr":
            l[8] = re.sub("/", " ", locip.with_netmask)
        else:
            l[8] = locip.with_prefixlen
        # Test System IP.
        ipaddress.ip_address(args.s)
        # Test Gateway IP.
        ipaddress.ip_address(args.g)
        # Test DNS.
        if args.d == "Skip":
            pass
        else:
            ipaddress.ip_address(args.d)
    # ValueError is passed from int(args.p), int(args.i), IPv4Interface() object, and ip_address() functions.
    except ValueError:
        sys.exit(
            "Invalid Input: Parameters are incorrect, or Local IP is given a Subnet Mask instead of a Prefix or an out of range Prefix."
        )
    return l
```

-	The create_txt(conf) function does the following:
    - It takes in the ordered list of arguments.
    - It checks the specified device type.
    - Depending on the specified device type, it iterates over its lines.
    - The input text files are configured as follows:
        - For all the input text files, the commands take in arguments in the same order. However, a special case exists for the vBond Orchestrator as it cannot be configured with port offset which makes the line for the port offset command non-existent.
        - Commands that require nothing to be added end with “&” which is replaced during the for loop iterations with “”.
        - Commands that are not ending with “&” are appended by the arguments specified by the user during the for loop iterations. A special case exists for the vBond Orchestrator where “_” is replaced by the vBond IP Address/Domain Name.
    - Depending on the line, a “&” is removed or an argument is added (or a “_” is replaced for the vBond Orchestrator). The output of this line is then appended into a list.
    - Sometimes a line may be skipped because an optional argument wasn’t specified (such as the Port Offset or the DNS). When this occurs, the line is not appended to the output list.
    - Finally, the function takes the output list and creates a new text file (or overwrites a previously created one) “output.txt” with the initial configuration of the SD-WAN device using a for loop.

```ruby
def create_txt(conf):
    out = []
    k = 1
    # According to the type of the device, we'll open the unconfigured text file, configure each line in it and write onto a new text file.
    with open(f"{conf[0]}.txt") as test:
        lines = test.readlines()
        for i in lines:
            if i.endswith("&\n") or i.endswith(
                "&"
            ):  # Check if the value is configurable -which are values ending with &-, if so, remove the &.
                i = re.sub("&", "", i)
                out.append(i)
            elif re.search(
                "_", i
            ):  # To add the vBond IP for the vBond's configuration.
                i = re.sub("_", conf[5], i)
                out.append(i)
                k += 1
            elif re.search(
                "(port-offset|dns|name-server)", i
            ):  # To skip these configurations if they were not inserted by the user.
                if conf[k] == "Skip" and conf[0].lower() != "vbond":
                    k += 1
                elif (
                    k == 6 and conf[0].lower() == "vbond"
                ):  # vBond file has no port-offset, so you have to skip the "Skip" value of the port-offset in the arguments list.
                    k += 1
                    if conf[k] == "Skip":
                        k += 1
                    else:
                        i = f"{i.strip()} {conf[k]}\n"
                        out.append(i)
                        k += 1
                else:
                    i = f"{i.strip()} {conf[k]}\n"
                    out.append(i)
                    k += 1
            else:
                i = f"{i.strip()} {conf[k]}\n"
                out.append(i)
                k += 1
    with open("output.txt", "w") as test:
        for i in out:
            test.write(i)
```
