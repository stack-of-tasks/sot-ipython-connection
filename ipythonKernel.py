from ipykernel.kernelapp import launch_new_instance

def main():
    # The IPython kernel's user namespace will be initialized with the
    # variables contained in this dictionary:
    namespace = dict(
        a = 0,
        b = 54
    )
    launch_new_instance(user_ns=namespace)

    # 2nd try (successful):
    # ~/.ipython/profile_default/startup/init_lsst.py will be
    # executed during IPython setup
    #launch_new_instance() 

if __name__ == "__main__" :
    main()
