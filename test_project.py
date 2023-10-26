from project import cleaner1, cleaner2, create_txt
from argparse import Namespace
import pytest


def test_cleaner1():
    # Test correct input with all parameters.
    args = Namespace(
        t="vsmart",
        n="vSmart",
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="0",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    assert cleaner1(args) == True
    # Test correct input without unrequired parameters.
    args = Namespace(
        t="vsmart",
        n="vSmart",
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="Skip",
        d="Skip",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    assert cleaner1(args) == True
    # Test correct input without some of the required parameters.
    args = Namespace(
        t="vsmart",
        n="vSmart",
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v=None,
        p="0",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    with pytest.raises(SystemExit):
        cleaner1(args)


def test_cleaner2():
    # Test correct input with all parameters with csr prefix to subnet.
    args = Namespace(
        t="csr",
        n="CSR",
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="0",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    assert cleaner2(args) == [
        "csr",
        "CSR",
        "3.3.3.3",
        "100",
        "HTITEST",
        "htitest.ddns.net",
        "0",
        "8.8.8.8",
        "192.168.1.201 255.255.255.0",
        "192.168.1.1",
    ]
    # Test port offset with vBond device type.
    args = Namespace(
        t="vbond",
        n="vBond",
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="1",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    with pytest.raises(SystemExit):
        cleaner2(args)
    # Test incorrect Type parameter.
    args_t = Namespace(
        t="vsmartt",
        n="vSmart",
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="0",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    with pytest.raises(SystemExit):
        cleaner2(args_t)
    # Test out of range Hostname parameter.
    args_n = Namespace(
        t="vsmart",
        n="h" * 33,
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="0",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    with pytest.raises(SystemExit):
        cleaner2(args_n)
    # Test incorrect System IP parameter.
    args_s = Namespace(
        t="vsmart",
        n="vSmart",
        s="cat",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="0",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    with pytest.raises(SystemExit):
        cleaner2(args_s)
    # Test out of range Site ID parameter.
    args_i = Namespace(
        t="vsmart",
        n="vSmart",
        s="3.3.3.3",
        i="4294967299",
        o="HTITEST",
        v="htitest.ddns.net",
        p="0",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    with pytest.raises(SystemExit):
        cleaner2(args_i)
    # Test incorrect type of Site ID parameter.
    args_i = Namespace(
        t="vsmart",
        n="vSmart",
        s="3.3.3.3",
        i="cat",
        o="HTITEST",
        v="htitest.ddns.net",
        p="0",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    with pytest.raises(SystemExit):
        cleaner2(args_i)
    # Test out of range Organization Name parameter.
    args_o = Namespace(
        t="vsmart",
        n="vSmart",
        s="3.3.3.3",
        i="100",
        o="h" * 65,
        v="htitest.ddns.net",
        p="0",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    with pytest.raises(SystemExit):
        cleaner2(args_o)
    # Test out of range Port Offset parameter.
    args_p = Namespace(
        t="vsmart",
        n="vSmart",
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="20",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    with pytest.raises(SystemExit):
        cleaner2(args_p)
    # Test incorrect type of Port Offset parameter.
    args_p = Namespace(
        t="vsmart",
        n="vSmart",
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="cat",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    with pytest.raises(SystemExit):
        cleaner2(args_p)
    # Test incorrect DNS parameter.
    args_d = Namespace(
        t="vsmart",
        n="vSmart",
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="0",
        d="cat",
        l="192.168.1.201/24",
        g="192.168.1.1",
    )
    with pytest.raises(SystemExit):
        cleaner2(args_d)
    # Test incorrect Local IP parameter.
    args_l = Namespace(
        t="vsmart",
        n="vSmart",
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="0",
        d="8.8.8.8",
        l="cat",
        g="192.168.1.1",
    )
    with pytest.raises(SystemExit):
        cleaner2(args_l)
    args_l = Namespace(
        t="vsmart",
        n="vSmart",
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="0",
        d="8.8.8.8",
        l="192.168.1.201 255.255.255.0",
        g="192.168.1.1",
    )
    with pytest.raises(SystemExit):
        cleaner2(args_l)
    # Test incorrect Gateway IP parameter.
    args_g = Namespace(
        t="vsmart",
        n="vSmart",
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="0",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="cat",
    )
    with pytest.raises(SystemExit):
        cleaner2(args_g)
    args_g = Namespace(
        t="vsmart",
        n="vSmart",
        s="3.3.3.3",
        i="100",
        o="HTITEST",
        v="htitest.ddns.net",
        p="0",
        d="8.8.8.8",
        l="192.168.1.201/24",
        g="192.168.1.1/24",
    )
    with pytest.raises(SystemExit):
        cleaner2(args_g)


def test_create_txt():
    # Case 1 vSmart or vManage
    # With DNS + Port Offset
    l = [
        "vsmart",
        "vSmart",
        "3.3.3.3",
        "100",
        "HTITEST",
        "htitest.ddns.net",
        "0",
        "8.8.8.8",
        "192.168.1.201/24",
        "192.168.1.1",
    ]
    create_txt(l)
    with open("output.txt") as test:
        lines = test.readlines()
        assert lines[0] == "config terminal\n"
        assert lines[2] == "host-name vSmart\n"
        assert lines[7] == "port-offset 0\n"
        assert lines[8] == "vpn 0\n"
        assert lines[12] == "ip add 192.168.1.201/24\n"
        assert lines[18] == "commit and-quit"
    # Without DNS or Port Offset
    l = [
        "vsmart",
        "vSmart",
        "3.3.3.3",
        "100",
        "HTITEST",
        "htitest.ddns.net",
        "Skip",
        "Skip",
        "192.168.1.201/24",
        "192.168.1.1",
    ]
    create_txt(l)
    with open("output.txt") as test:
        lines = test.readlines()
        assert lines[0] == "config terminal\n"
        assert lines[2] == "host-name vSmart\n"
        assert lines[7] == "vpn 0\n"
        assert lines[8] == "int eth0\n"
        assert lines[12] == "allow-service all\n"
        assert lines[16] == "commit and-quit"
    # Case 2 vBond
    # With DNS
    l = [
        "vbond",
        "vBond",
        "3.3.3.3",
        "100",
        "HTITEST",
        "htitest.ddns.net",
        "Skip",
        "8.8.8.8",
        "192.168.1.201/24",
        "192.168.1.1",
    ]
    create_txt(l)
    with open("output.txt") as test:
        lines = test.readlines()
        assert lines[0] == "config\n"
        assert lines[2] == "host-name vBond\n"
        assert lines[7] == "vpn 0\n"
        assert lines[8] == "dns 8.8.8.8\n"
        assert lines[12] == "no tunnel-interface\n"
        assert lines[15] == "commit and-quit"
    # Without DNS
    l = [
        "vbond",
        "vBond",
        "3.3.3.3",
        "100",
        "HTITEST",
        "htitest.ddns.net",
        "Skip",
        "Skip",
        "192.168.1.201/24",
        "192.168.1.1",
    ]
    create_txt(l)
    with open("output.txt") as test:
        lines = test.readlines()
        assert lines[0] == "config\n"
        assert lines[2] == "host-name vBond\n"
        assert lines[7] == "vpn 0\n"
        assert lines[8] == "int ge0/0\n"
        assert lines[12] == "exit\n"
        assert lines[14] == "commit and-quit"
    # Case 3 CSR
    # With DNS + Port Offset
    l = [
        "csr",
        "CSR",
        "3.3.3.3",
        "100",
        "HTITEST",
        "htitest.ddns.net",
        "0",
        "8.8.8.8",
        "192.168.1.201 255.255.255.0",
        "192.168.1.1",
    ]
    create_txt(l)
    with open("output.txt") as test:
        lines = test.readlines()
        assert lines[0] == "enable\n"
        assert lines[2] == "hostname CSR\n"
        assert lines[8] == "system port-offset 0\n"
        assert lines[11] == "ip name-server 8.8.8.8\n"
        assert lines[13] == "ip address 192.168.1.201 255.255.255.0\n"
        assert lines[15] == "ip route 0.0.0.0 0.0.0.0 192.168.1.1\n"
        assert lines[23] == "sdwan\n"
        assert lines[31] == "end"
    # Without DNS or Port Offset
    l = [
        "csr",
        "CSR",
        "3.3.3.3",
        "100",
        "HTITEST",
        "htitest.ddns.net",
        "Skip",
        "Skip",
        "192.168.1.201 255.255.255.0",
        "192.168.1.1",
    ]
    create_txt(l)
    with open("output.txt") as test:
        lines = test.readlines()
        assert lines[0] == "enable\n"
        assert lines[2] == "hostname CSR\n"
        assert lines[8] == "commit\n"
        assert lines[11] == "ip address 192.168.1.201 255.255.255.0\n"
        assert lines[13] == "ip route 0.0.0.0 0.0.0.0 192.168.1.1\n"
        assert lines[15] == "interface Tunnel1\n"
        assert lines[23] == "tunnel-interface\n"
        assert lines[29] == "end"
