from ipykernel.kernelapp import launch_new_instance

def main():
    # The IPython kernel's user namespace will be initialized with the
    # variables contained in this dictionary:
    namespace = dict(
        a = 0,
        b = 54
    )
    launch_new_instance(user_ns=namespace)

if __name__ == "__main__" :
    main()
