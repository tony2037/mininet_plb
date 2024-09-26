# then to use one (as root):  insmod <module_name.ko>

obj-m := hook_plb.o


all:
	make -C /usr/lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /usr/lib/modules/$(shell uname -r)/build M=$(PWD) clean

install:
	sudo insmod hook_plb.ko

uninstall:
	sudo rmmod hook_plb.ko

list:
	sudo lsmod