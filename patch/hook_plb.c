#define pr_fmt(fmt) "%s: " fmt, __func__

#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/kprobes.h>

static int ewma_ratio = 0;
static int lambda_denominator = 2;
static int lambda_numerator = 1;


static char symbol[KSYM_NAME_LEN] = "tcp_plb_update_state";
module_param_string(symbol, symbol, KSYM_NAME_LEN, 0644);

/* For each probe you need to allocate a kprobe structure */
static struct kprobe kp = {
	.symbol_name	= symbol,
};

/*
void tcp_plb_update_state(const struct sock *sk, struct tcp_plb_state *plb,
+			  const int cong_ratio)
*/
/* kprobe pre_handler: called just before the probed instruction is executed */
static int __kprobes handler_pre(struct kprobe *p, struct pt_regs *regs)
{
    int cong_ratio = regs->dx;
	ewma_ratio = (ewma_ratio * (lambda_denominator-lambda_numerator) + cong_ratio * lambda_numerator) / lambda_denominator;
	regs->dx = ewma_ratio;
    pr_info("<%s> cong_ratio: %d\n", p->symbol_name, regs->dx);

	/* A dump_stack() here will give a stack backtrace */
	return 0;
}

/* kprobe post_handler: called after the probed instruction is executed */
static void __kprobes handler_post(struct kprobe *p, struct pt_regs *regs,
				unsigned long flags)
{
	pr_info("exit: <%s> p->addr = 0x%p, flags = 0x%lx\n",
		p->symbol_name, p->addr, regs->flags);
}

static int __init kprobe_init(void)
{
	int ret;
	kp.pre_handler = handler_pre;
	kp.post_handler = NULL;

	ret = register_kprobe(&kp);
	if (ret < 0) {
		pr_err("register_kprobe failed, returned %d\n", ret);
		return ret;
	}
	pr_info("Planted kprobe at %p\n", kp.addr);
	return 0;
}

static void __exit kprobe_exit(void)
{
	unregister_kprobe(&kp);
	pr_info("kprobe at %p unregistered\n", kp.addr);
}

module_init(kprobe_init)
module_exit(kprobe_exit)
MODULE_LICENSE("GPL");