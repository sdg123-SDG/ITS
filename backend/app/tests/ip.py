import stun

def get_ip_via_stun():
    """
    [辅助函数] 获取本机公网 IP
    """
    try:
        # 正确用法！
        nat_type, external_ip, external_port = stun.get_ip_info()
        return external_ip
    except Exception as e:
        print(f"STUN 获取失败: {e}")
        return None

if __name__ == "__main__":
    print("你的公网IP：", get_ip_via_stun())