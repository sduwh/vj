"""杭州电子科技大学"""

name = "HDU"

problem_url = "http://acm.hdu.edu.cn/showproblem.php?pid=%d"

encoding = "gbk"

minid = 1000

maxid = 10000

regexp = {
    "title": r"<h1 style='color:#1A5CC8'>(.+?)<\/h1>",
    "timelimit": r"Time Limit: \d+\/(\d+) MS",
    "memorylimit": r"Memory Limit: \d+\/(\d+) K",
    "description": r"Problem Description<\/div> <div class=panel_content>([.\s\S]+?)<\/div><div class=panel_bottom>",
    "input": r"Input<\/div> <div class=panel_content>([.\s\S]+?)<\/div><div class=panel_bottom>",
    "output": r"Output<\/div> <div class=panel_content>([.\s\S]+?)<\/div><div class=panel_bottom>",
    "sampleinput": r"Sample Input<\/div><div class=panel_content><pre>([.\s\S]+?)<\/pre><\/div><div class=panel_bottom>",
    "sampleoutput": r"Sample Output<\/div><div class=panel_content><pre>([.\s\S]+?)<\/pre><\/div><div class=panel_bottom>",
    "source": r"Source</div> <div class=panel_content> <a href=.+?>([.\s\S]+?)</a> </div>",
}

def replace_src(description):
    return description.replace(r"src=", r"src=http://acm.hdu.edu.cn/")
