"""山东理工大学"""

name = "SDUT"

problem_url = "http://acm.sdut.edu.cn/onlinejudge2/index.php/Home/Index/problemdetail/pid/%d.html"

encoding = "utf8"

minid = 1000

maxid = 10000

regexp = {
    "title": r'<h3 class="problem-header">(.+?)</h3>',
    "timelimit": r'<span class="user-black">Time Limit:&nbsp;(\d+?) ms</span>',
    "memorylimit": r'<span class="user-black" style="margin-left: 12px;">Memory Limit:&nbsp;(\d+?) KiB</span>',
    "description": r'<h4>Problem Description</h4>[\s\S]*?<div class="prob-content">([.\s\S]+?)</div>[\s\S]*?<h4>Input',
    "input": r'<h4>Input</h4>[\s\S]*?<div class="prob-content">([.\s\S]+?)</div>[\s\S]*?<h4>Output',
    "output": r'<h4>Output</h4>[\s\S]*?<div class="prob-content">([.\s\S]+?)</div>[\s\S]*?<h4>Sample Input',
    "sampleinput": r'<h4>Sample Input</h4>[\s\S]*?<div class="prob-content">[\s\S]*?<pre>([.\s\S]+?)</pre>[\s\S]*?</div>[\s\S]*?<h4>Sample Output',
    "sampleoutput": r'<h4>Sample Output</h4>[\s\S]*?<div class="prob-content">[\s\S]*?<pre>([.\s\S]+?)</pre>[\s\S]*?</div>[\s\S]*?<h4>Hint',
    "source": r'<h4>Author</h4>[\s\S]*?<div class="prob-content">([.\s\S]+?)</div>',
}

def replace_src(description):
    return description.replace(r'src="/', r'src="http://acm.sdut.edu.cn/')
