"""北京大学"""

name = "POJ"

problem_url = "http://poj.org/problem?id=%d"

encoding = "utf8"

minid = 1000

maxid = 10000

regexp = {
    "title": r'<div class="ptt" lang="en-US">(.+?)<\/div>',
    "timelimit": r'Time Limit:<\/b> (\d+?)MS',
    "memorylimit": r'Memory Limit:<\/b> (\d+?)K',
    "description": r'<p class="pst">Description<\/p><div class="ptx" lang="en-US">([.\s\S]+?)<\/div><p class="pst">Input',
    "input": r'<p class="pst">Input<\/p><div class="ptx" lang="en-US">([.\s\S]+?)<\/div><p class="pst">Output',
    "output": r'<p class="pst">Output<\/p><div class="ptx" lang="en-US">([.\s\S]+?)<\/div><p class="pst">Sample Input',
    "sampleinput": r'<p class="pst">Sample Input<\/p><pre class="sio">([.\s\S]+?)<\/pre><p class="pst">Sample Output',
    "sampleoutput": r'<p class="pst">Sample Output<\/p><pre class="sio">([.\s\S]+?)<\/pre><p class="pst">',
    "source": r'<p class="pst">Source</p><div class="ptx" lang="en-US"><a href=.+?>([.\s\S]*?)</a></div>',
}

def replace_src(description):
    import re
    if len(re.findall(r'src="', description)) > 0:
        return description.replace('src="', 'src="http://poj.org/')
    if len(re.findall(r"src='", description)) > 0:
        return description.replace("src='", "src='http://poj.org/")
    if len(re.findall(r"src=", description)) > 0:
        return description.replace("src=", "src=http://poj.org/")
    return description
