import support.HDU

import config

code = '''
#include <stdio.h>

int main()
{
    int a,b;
    scanf("%d %d",&a, &b);
    printf("%d\n",a+b);
    return 0;
}
'''
print(support.HDU.Runner(config.accounts['HDU'], 3, 1).judge(1000, 0, code))
