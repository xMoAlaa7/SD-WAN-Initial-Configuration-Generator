import re
import argparse
import ipaddress
import sys


def main():
    configs = inputs()
    cleaner1(configs)
    configs_clean = cleaner2(configs)
    create_txt(configs_clean)


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


if __name__ == "__main__":
    main()
