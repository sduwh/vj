(function () {
    // 与首页相关的变量集合
    var common = {
        'curIndex': 0,
        'pageName': ['instruction-page', 'first-ac-page', 'last-ac-page', 'difficult-ac-page', 'contest-page', 'rank-page', 'achievement-page', 'time-page'],
        'indexURL': '/api/user/record',
        'otherURL': '/api/user/record',
        // 'logoutURL': '../../controllers/logout.json',
        'resetURL': '/api/user/resetpassword',
        'improveProblemURL': 'http://acm.wh.sdu.edu.cn:8000',
        'improveContestURL': 'http://acm.wh.sdu.edu.cn:8000',
        'indexData': null,
        'otherData': null,
        'dom': {
            'type': $('.wrapper .instruction-page .info .type')
        },
        'typeContent': [
            'Acm', '({',
            'user', ': {',
            'name', ': ', '6', ',',
            'acception', ': ', '10', ',',
            'submission', ': ', '14', ',',
            'accept_rate', ': ', '18',
            '},',
            'target', ': {',
            'ACM_ICPC', ': ', "'Faster, Higher and Stronger'",
            '}',
            '})'
        ]
    };

    // 与 first_ac_page 页相关的变量集合
    var firstAcPageVar = {
        'dom': {
            'desc': $('.wrapper .first-ac-page .info .first-ac-page_title .desc'),
            'descNone': $('.wrapper .first-ac-page .info .first-ac-page_title .desc-none'),
            'firstAcPageCode': $('.wrapper .first-ac-page .info .first-ac-page_code'),
            'firstAcPagePic': $('.wrapper .first-ac-page .info .first-ac-page_pic'),
            'year': $('.wrapper .first-ac-page .info .first-ac-page_title .desc .time-1'),
            'month': $('.wrapper .first-ac-page .info .first-ac-page_title .desc .time-3'),
            'day': $('.wrapper .first-ac-page .info .first-ac-page_title .desc .time-5'),
            'yearNone': $('.wrapper .first-ac-page .info .first-ac-page_title .desc-none .time-1'),
            'monthNone': $('.wrapper .first-ac-page .info .first-ac-page_title .desc-none .time-3'),
            'dayNone': $('.wrapper .first-ac-page .info .first-ac-page_title .desc-none .time-5'),
            'title': $('.wrapper .first-ac-page .info .first-ac-page_code .title p a'),
            'code': $('.wrapper .first-ac-page .info .first-ac-page_code .code .scroll-wrapper .code-content code')
        }
    };

    // 与 last_ac_page 页面相关的变量集合
    var lastAcPageVar = {
        'dom': {
            'desc': $('.wrapper .last-ac-page .info .last-ac-page_title .desc'),
            'descNone': $('.wrapper .last-ac-page .info .last-ac-page_title .desc-none'),
            'lastAcPageCode': $('.wrapper .last-ac-page .info .last-ac-page_code'),
            'lastAcPagePic': $('.wrapper .last-ac-page .info .last-ac-page_pic'),
            'year': $('.wrapper .last-ac-page .info .last-ac-page_title .desc .time-1'),
            'month': $('.wrapper .last-ac-page .info .last-ac-page_title .desc .time-3'),
            'day': $('.wrapper .last-ac-page .info .last-ac-page_title .desc .time-5'),
            'yearNone': $('.wrapper .last-ac-page .info .last-ac-page_title .desc-none .time-1'),
            'monthNone': $('.wrapper .last-ac-page .info .last-ac-page_title .desc-none .time-3'),
            'dayNone': $('.wrapper .last-ac-page .info .last-ac-page_title .desc-none .time-5'),
            'title': $('.wrapper .last-ac-page .info .last-ac-page_code .title p a'),
            'code': $('.wrapper .last-ac-page .info .last-ac-page_code .code .scroll-wrapper .code-content code')
        }
    };

    // 与 difficult_ac_page 页面相关的变量集合
    var difficultAcPageVar = {
        'dom': {
            'desc': $('.wrapper .difficult-ac-page .info .difficult-ac-page_title .desc'),
            'descNone': $('.wrapper .difficult-ac-page .info .difficult-ac-page_title .desc-none'),
            'difficultAcPageCode': $('.wrapper .difficult-ac-page .info .difficult-ac-page_code'),
            'difficultAcPagePic': $('.wrapper .difficult-ac-page .info .difficult-ac-page_pic'),
            'times': $('.wrapper .difficult-ac-page .info .difficult-ac-page_title .desc .times'),
            'title': $('.wrapper .difficult-ac-page .info .difficult-ac-page_code .title p a'),
            'code': $('.wrapper .difficult-ac-page .info .difficult-ac-page_code .code .scroll-wrapper .code-content code')
        }
    };

    // 与 contest_page 页面相关的变量集合
    var contestPageVar = {
        'dom': {
            'scrollWrapper': $('.wrapper .contest-page .info .list .scroll-wrapper'),
            'face': $('.wrapper .contest-page .info .list .face'),
            'templateWrap': $('.wrapper .contest-page .info .list .scroll-wrapper ul')
        }
    };

    // 与 rank-page 页面相关的变量集合
    var rankPageVar = {
        'dom': {
            'li': $('.wrapper .rank-page .info .container .cube-wrap .cube .cube-face ul li'),
            'prevUl': $('.wrapper .rank-page .info .container .cube-wrap .cube .top ul'),
            'nextUl': $('.wrapper .rank-page .info .container .cube-wrap .cube .bottom ul'),
            'prevHint': $('.wrapper .rank-page .info .container .cube-wrap .cube .top .hint'),
            'nextHint': $('.wrapper .rank-page .info .container .cube-wrap .cube .bottom .hint')
        }
    };

    // 与 achievement-page 页面相关的变量集合
    var achievementPageVar = {
        'dom': {
            'liWrap': $('.wrapper .achievement-page .info .wall .scroll-wrapper ul')
        },
        'achievements': {
            // is_ac
            'isAc': {
                'title': 'ACCEPT',
                'desc': '在平台AC至少一题'
            },

            // is_wa
            'isWa': {
                'title': 'WA',
                'desc': '在平台WA至少一题'
            },

            // common.indexData.total_ac
            'ac_10': {
                'title': '10 ACCEPT',
                'desc': '在平台AC至少10题'
            },
            'ac_50': {
                'title': '50 ACCEPT',
                'desc': '在平台AC至少50题'
            },
            'ac_100': {
                'title': '100 ACCEPT',
                'desc': '在平台AC至少100题'
            },
            'ac_200': {
                'title': '200 ACCEPT',
                'desc': '在平台AC至少200题'
            },
            'ac_300': {
                'title': '300 ACCEPT',
                'desc': '在平台AC至少300题'
            },
            'ac_500': {
                'title': '500 ACCEPT',
                'desc': '在平台AC至少500题'
            },
            'ac_1000': {
                'title': '1000 ACCEPT',
                'desc': '在平台AC至少1000题'
            },

            // continuous_no_ac_cnt
            'continuousNoAc': {
                'title': 'DIFFICULT',
                'desc': '某道题至少连续提交10次都不通过'
            },

            // once_ac_cnt
            'onceAc_5': {
                'title': '5 ONCE ACCEPT',
                'desc': '首次提交AC的题目超过5道'
            },
            'onceAc_10': {
                'title': '10 ONCE ACCEPT',
                'desc': '首次提交AC的题目超过10道'
            },
            'onceAc_20': {
                'title': '20 ONCE ACCEPT',
                'desc': '首次提交AC的题目超过20道'
            },
            'onceAc_50': {
                'title': '50 ONCE ACCEPT',
                'desc': '首次提交AC的题目超过50道'
            },
            'onceAc_100': {
                'title': '100 ONCE ACCEPT',
                'desc': '首次提交AC的题目超过100道'
            },

            // once_wa_cnt
            'onceWa_10': {
                'title': '10 ONCE WA',
                'desc': '首次提交WA的题目超过10道'
            },
            'onceWa_20': {
                'title': '20 ONCE WA',
                'desc': '首次提交WA的题目超过20道'
            },
            'onceWa_50': {
                'title': '50 ONCE WA',
                'desc': '首次提交WA的题目超过50道'
            },
            'onceWa_100': {
                'title': '100 ONCE WA',
                'desc': '首次提交WA的题目超过100道'
            },

            // contest {is_first: true, is_last: }
            'hasContestFirst': {
                'title': 'CONTEST FIRST',
                'desc': '在平台比赛中取得过第一名'
            },
            'hasContestLast': {
                'title': 'CONTEST LAST',
                'desc': '在平台比赛中取得过最后一名'
            },

            // festival {valentine: , newyear: , single: }
            'valentine': {
                'title': 'VALENTINE',
                'desc': '情人节还在做题'
            },
            'newyear': {
                'title': 'NEW YEAR',
                'desc': '元旦节还在做题'
            },
            'single': {
                'title': 'SINGLE',
                'desc': '光棍节还在做题'
            }
        }
    }

    // 与 time-page 页面相关的变量集合
    var timePageVar = {
        'dom': {
            'dayText': $('.wrapper .time-page .info .clock-body .days .text1')
        }
    }

    // 与页面切换相关的变量集合
    var changePageVar = {
        'dom': {
            'li': $('.wrapper .index-bar ul li'),
            'angleDown': $('.wrapper .page .angle-down span')
        }
    }

    // 与 function-bar 相关的变量集合
    var fnBarVar = {
        'dom': {
            'logout': $('.wrapper .function-bar .scal-wrap .logout a'),
            'reset': $('.wrapper .function-bar .scal-wrap .reset a'),
            'alertWrap': $('.wrapper .alert-wrapper'),
            'alertBox': $('.wrapper .alert-wrapper .alert-box'),
            'correct': $('.wrapper .alert-wrapper .correct'),
            'oldPas': $('.wrapper .alert-wrapper .alert-box .old-password input'),
            'newPas': $('.wrapper .alert-wrapper .alert-box .new-password input'),
            'newPasRe': $('.wrapper .alert-wrapper .alert-box .new-password-repeat input'),
            'oldPasHint': $('.wrapper .alert-wrapper .alert-box .old-password .hint'),
            'newPasHint': $('.wrapper .alert-wrapper .alert-box .new-password .hint'),
            'rePasHint': $('.wrapper .alert-wrapper .alert-box .new-password-repeat .hint'),
            'confirmBtn': $('.wrapper .alert-wrapper .alert-box .btn .confirm'),
            'cancel': $('.wrapper .alert-wrapper .alert-box .btn .cancel')
        },
        'oldPasHintText_1': '原密码错误!',
        'oldPasHintText_2': '请输入原密码!',
        'newPasHintText_1': '两次输入的密码不一致!',
        'newPasHintText_2': '请输入新密码!',
        'newPasReHintText_1': '两次密码输入不一致!',
        'newPasReHintText_2': '请输入确认密码!'
    }

    // 页面初始化
    function init() {
        getIndexData();

        // 不能在这里获取 OtherData，因为与 otherData 相关的操作除了基于 otherData 的数据，还基于 indexData 的数据，所以要保证在 indexData 数据加在完成之后才能执行相应的操作
        // getOtherData();

        // logout();
        reset();
    }

    // 获取首页数据后，将数据保存
    function improveIndexData(data) {
        common.indexData = data;
    }

    // 拿到首页数据后，完善打印数组的内容
    function improveTypeContent() {
        common.typeContent[6] = "'" +  common.indexData.nickname + "'";
        common.typeContent[10] = common.indexData.total_ac + '';
        common.typeContent[14] = common.indexData.total_sub + '';
        common.typeContent[18] = "'" + ((common.indexData.total_ac / common.indexData.total_sub) * 100).toFixed(2) + "%'";
    }

    // 把 indexData 中的注册时间 registration_time 由时间戳改成日期格式
    function improveRegistTime() {
        var date = new Date(common.indexData.registration_time);
        var y = date.getFullYear();
        var m = date.getMonth() + 1;
        var d = date.getDate();
        common.indexData.registration_time_improved = y + ' ' + m + ' ' + d;
    }

    // 拿到首页数据后，完善需要完善的数据
    function improveData(data) {
        improveIndexData(data);
        improveTypeContent();
        improveRegistTime();
    }

    // 打印首页 instruction-page 页面内容
    function typing() {
        var index = 0,
            typeLen = common.dom.type.length;
        print(common.typeContent[index], common.dom.type[index]);

        function print(str, ele) {
            if (index === typeLen) {
                return;
            }
            var strLen = str.length,
                cnt = 1;
            var t = setInterval(function () {
                if (cnt === strLen + 1) {
                    clearInterval(t);
                    index++;
                    print(common.typeContent[index], common.dom.type[index]);
                } else {
                    ele.innerHTML = str.substring(0, cnt);
                    cnt++;
                }
            }, 80);
        }
    }

    // 渲染首页 instruction-page 页面
    function renderInstructionPage() {
        typing();
    }

    // 获取首页 instruction-page 的数据
    function getIndexData() {
        $.ajax({
            'type': 'GET',
            'data': 'type=index',
            'url': common.indexURL,
            'dataType': 'json',
            'success': function (data) {
                // 加载其他页面需要的数据 otherData
                getOtherData();
                // 加载页面切换的功能
                changeIndex();
                // 执行与首页上依赖 indexData 数据的操作
                improveData(data);
                renderInstructionPage();
            }
        });
    }

    // 实现页面的切换
    function changePage(cur, tar) {
        var curPage = common.pageName[cur];
        var tarPage = common.pageName[tar];
        var curPageDom = $('.' + curPage);
        var tarPageDom = $('.' + tarPage);

        // 更新当前 index
        common.curIndex = tar;

        // 更改 index-bar
        $(changePageVar.dom.li[cur]).removeClass('active');
        $(changePageVar.dom.li[tar]).addClass('active');

        // 切换页面
        curPageDom.fadeOut(1000);
        tarPageDom.fadeIn(1000);
    }

    // 当通过侧边索引栏切换页面时，确定当前页和目标页
    function selectIndexBar() {
        changePageVar.dom.li.on('click', function () {
            var tarIndex = $(this).index();
            if (tarIndex != common.curIndex) {
                changePage(common.curIndex, tarIndex)
            }
        });
    }

    // 当通过点击向下按钮切换时，确定当前页和目标页
    function touchAngleDown() {
        changePageVar.dom.angleDown.on('click', function () {
            changePage(common.curIndex, common.curIndex + 1);
        });
    }

    // 实现页面索引的切换
    function changeIndex() {
        selectIndexBar();
        touchAngleDown();
        // scrollPage();
    }

    // 拿到其他数据后，将数据保存
    function improveOtherData(data) {
        common.otherData = data;
    }


    // 拿到其他数据后，对其他数据进行进一步的补充完善
    function improveRemainData(data) {
        improveOtherData(data);
    }

    // 获取除首页数据外的其他页的数据
    function getOtherData() {
        $.ajax({
            'type': 'GET',
            'data': 'type=others',
            'url': common.otherURL,
            'dataType': 'json',
            'success': function (data) {
                improveRemainData(data);
                renderOtherPage();
            }
        });
    }

    // 渲染 first-ac-page
    function renderFirstAcPage() {
        if (!common.otherData.first_ac) {
            //  根据有没有 ac 决定显示什么样式
            firstAcPageVar.dom.desc.css('display', 'none');
            firstAcPageVar.dom.firstAcPageCode.css('display', 'none');
            firstAcPageVar.dom.descNone.css('display', 'block');
            firstAcPageVar.dom.firstAcPagePic.css('display', 'block');

            //  填入相应的时间
            var timeArr = common.indexData.registration_time_improved.split(' ');
            firstAcPageVar.dom.yearNone.html(timeArr[0]);
            firstAcPageVar.dom.monthNone.html(timeArr[1]);
            firstAcPageVar.dom.dayNone.html(timeArr[2]);
        } else {
            firstAcPageVar.dom.desc.css('display', 'block');
            firstAcPageVar.dom.firstAcPageCode.css('display', 'block');
            firstAcPageVar.dom.descNone.css('display', 'none');
            firstAcPageVar.dom.firstAcPagePic.css('display', 'none');

            // 填入相应的内容
            var timeArr = common.otherData.first_ac.time.split(' ');
            firstAcPageVar.dom.year.html(timeArr[0]);
            firstAcPageVar.dom.month.html(timeArr[1]);
            firstAcPageVar.dom.day.html(timeArr[2]);
            firstAcPageVar.dom.title.html(common.otherData.first_ac.title);
            firstAcPageVar.dom.title.prop('href', common.improveProblemURL + common.otherData.first_ac.url);

            var highlightCode = hljs.highlightAuto(common.otherData.first_ac.code).value;
            firstAcPageVar.dom.code.html(highlightCode);
        }
    }

    // 渲染 last-ac-page
    function renderLastAcPage() {
        if (!common.otherData.last_ac) {
            lastAcPageVar.dom.desc.css('display', 'none');
            lastAcPageVar.dom.lastAcPageCode.css('display', 'none');
            lastAcPageVar.dom.descNone.css('display', 'block');
            lastAcPageVar.dom.lastAcPagePic.css('display', 'block');

            var timeArr = common.indexData.registration_time_improved.split(' ');
            lastAcPageVar.dom.yearNone.html(timeArr[0]);
            lastAcPageVar.dom.monthNone.html(timeArr[1]);
            lastAcPageVar.dom.dayNone.html(timeArr[2]);
        } else {
            lastAcPageVar.dom.descNone.css('display', 'none');
            lastAcPageVar.dom.lastAcPagePic.css('display', 'none');
            lastAcPageVar.dom.desc.css('display', 'block');
            lastAcPageVar.dom.lastAcPageCode.css('display', 'block');

            var timeArr = common.otherData.last_ac.time.split(' ');
            lastAcPageVar.dom.year.html(timeArr[0]);
            lastAcPageVar.dom.month.html(timeArr[1]);
            lastAcPageVar.dom.day.html(timeArr[2]);
            lastAcPageVar.dom.title.html(common.otherData.last_ac.title);
            lastAcPageVar.dom.title.prop('href', common.improveProblemURL + common.otherData.last_ac.url);

            var highlightCode = hljs.highlightAuto(common.otherData.last_ac.code).value;
            lastAcPageVar.dom.code.html(highlightCode);
        }
    }

    // 渲染 difficult-ac-page
    function renderDifficultPage() {
        if (!common.otherData.difficult_ac) {
            difficultAcPageVar.dom.desc.css('display', 'none');
            difficultAcPageVar.dom.difficultAcPageCode.css('display', 'none');
            difficultAcPageVar.dom.descNone.css('display', 'block');
            difficultAcPageVar.dom.difficultAcPagePic.css('display', 'block');
        } else {
            difficultAcPageVar.dom.descNone.css('display', 'none');
            difficultAcPageVar.dom.difficultAcPagePic.css('display', 'none');
            difficultAcPageVar.dom.desc.css('display', 'block');
            difficultAcPageVar.dom.difficultAcPageCode.css('display', 'block');

            difficultAcPageVar.dom.times.html(common.otherData.difficult_ac.none_ac_cnt);
            difficultAcPageVar.dom.title.html(common.otherData.difficult_ac.title);
            difficultAcPageVar.dom.title.prop('href', common.improveProblemURL + common.otherData.difficult_ac.url);

            var highlightCode = hljs.highlightAuto(common.otherData.difficult_ac.code).value;
            difficultAcPageVar.dom.code.html(highlightCode);
        }
    }

    // 渲染 contest-page
    function renderContestPage() {
        if (!common.otherData.contest_list) {
            contestPageVar.dom.scrollWrapper.css('display', 'none');
            contestPageVar.dom.face.css('display', 'block');
        } else {
            contestPageVar.dom.face.css('display', 'none');
            contestPageVar.dom.scrollWrapper.css('display', 'block');

            var listLen = common.otherData.contest_list.length;
            var htmlStr = '';
            for (var i = 0; i < listLen; i++) {
                var title = common.otherData.contest_list[i].title,
                    url = common.improveContestURL + common.otherData.contest_list[i].url,
                    rank = common.otherData.contest_list[i].rank,
                    desc = common.otherData.contest_list[i].description,
                    time = common.otherData.contest_list[i].time;
                var template = `
                    <li>
                        <div class="avatar"></div>
                        <div class="about">
                            <a href="${url}" class="name" title="${title}">${title}</a>
                            <p>
                                <span class="rank-pic"><img src="/static/img/rank-20.png"></span>
                                <span class="rank" title="排名:${rank}">${rank}</span>
                            </p>
                            <p>
                                <span class="desc-pic"><img src="/static/img/desc-20.png"></span>
                                <span class="desc" title="描述:${desc}">${desc}</span>
                            </p>
                            <p>
                                <span class="time-pic"><img src="/static/img/time-20.png"></span>
                                <span class="time" title="时间:${time}">${time}</span>
                            </p>
                        </div>
                    </li>
                `;
                htmlStr += template;
            }
            contestPageVar.dom.templateWrap.html(htmlStr);
        }
    }

    // 渲染 rank-page
    function renderRankPage() {
        // 自己的排名
        // nickname:
        // rank:
        // accept:
        // wa:
        rankPageVar.dom.li[1].innerHTML = 'nickname: ' + common.indexData.nickname;
        rankPageVar.dom.li[2].innerHTML = 'rank: ' + common.otherData.rank.my_rank;
        rankPageVar.dom.li[3].innerHTML = 'accept: ' + common.indexData.total_ac;
        rankPageVar.dom.li[4].innerHTML = 'wa: ' + common.indexData.total_wa;

        // ac 第一名
        rankPageVar.dom.li[6].innerHTML = 'nickname: ' + common.otherData.rank.other_person.ac_first.nickname;
        rankPageVar.dom.li[7].innerHTML = 'rank: ' + common.otherData.rank.other_person.ac_first.rank;
        rankPageVar.dom.li[8].innerHTML = 'accept: ' + common.otherData.rank.other_person.ac_first.total_ac;
        rankPageVar.dom.li[9].innerHTML = 'wa: ' + common.otherData.rank.other_person.ac_first.total_wa;

        // wa 第一名
        rankPageVar.dom.li[11].innerHTML = 'nickname: ' + common.otherData.rank.other_person.wa_first.nickname;
        rankPageVar.dom.li[12].innerHTML = 'rank: ' + common.otherData.rank.other_person.wa_first.rank;
        rankPageVar.dom.li[13].innerHTML = 'accept: ' + common.otherData.rank.other_person.wa_first.total_ac;
        rankPageVar.dom.li[14].innerHTML = 'wa: ' + common.otherData.rank.other_person.wa_first.total_wa;

        // 前一名
        if (common.otherData.rank.my_rank == 1 || common.otherData.rank.other_person.prev == null) {
            rankPageVar.dom.prevHint.css('display', 'block');
        } else {
            rankPageVar.dom.prevUl.css('display', 'block');
            rankPageVar.dom.li[16].innerHTML = 'nickname: ' + common.otherData.rank.other_person.prev.nickname;
            rankPageVar.dom.li[17].innerHTML = 'rank: ' + common.otherData.rank.other_person.prev.rank;
            rankPageVar.dom.li[18].innerHTML = 'accept: ' + common.otherData.rank.other_person.prev.total_ac;
            rankPageVar.dom.li[19].innerHTML = 'wa: ' + common.otherData.rank.other_person.prev.total_wa;
        }

        // 后一名
        if (common.otherData.rank.other_person.next == null) {
            rankPageVar.dom.nextHint.css('display', 'block');
        } else {
            rankPageVar.dom.nextUl.css('display', 'block');
            rankPageVar.dom.li[21].innerHTML = 'nickname: ' + common.otherData.rank.other_person.next.nickname;
            rankPageVar.dom.li[22].innerHTML = 'rank: ' + common.otherData.rank.other_person.next.rank;
            rankPageVar.dom.li[23].innerHTML = 'accept: ' + common.otherData.rank.other_person.next.total_ac;
            rankPageVar.dom.li[24].innerHTML = 'wa: ' + common.otherData.rank.other_person.next.total_wa;
        }
    }

    // 渲染 achievement-page
    function renderAchievementPage() {
        var classname = '';
        var htmlStr = '';
        for (key in achievementPageVar.achievements) {
            classname = key;
            switch (key) {
                case 'isAc':
                    classname += common.otherData.achievement.is_ac ? ' active' : '';
                    break;
                case 'isWa':
                    classname += common.otherData.achievement.is_wa ? ' active' : '';
                    break;
                case 'ac_10':
                    classname += common.indexData.total_ac >= 10 ? ' active' : '';
                    break;
                case 'ac_50':
                    classname += common.indexData.total_ac >= 50 ? ' active' : '';
                    break;
                case 'ac_100':
                    classname += common.indexData.total_ac >= 100 ? ' active' : '';
                    break;
                case 'ac_200':
                    classname += common.indexData.total_ac >= 200 ? ' active' : '';
                    break;
                case 'ac_300':
                    classname += common.indexData.total_ac >= 300 ? ' active' : '';
                    break;
                case 'ac_500':
                    classname += common.indexData.total_ac >= 500 ? ' active' : '';
                    break;
                case 'ac_1000':
                    classname += common.indexData.total_ac >= 1000 ? ' active' : '';
                    break;
                case 'continuousNoAc':
                    classname += common.otherData.achievement.continuous_none_ac_cnt >= 10 ? ' active' : '';
                    break;
                case 'onceAc_5':
                    classname += common.otherData.achievement.once_ac_cnt >= 5 ? ' active' : '';
                    break;
                case 'onceAc_10':
                    classname += common.otherData.achievement.once_ac_cnt >= 10 ? ' active' : '';
                    break;
                case 'onceAc_20':
                    classname += common.otherData.achievement.once_ac_cnt >= 20 ? ' active' : '';
                    break;
                case 'onceAc_50':
                    classname += common.otherData.achievement.once_ac_cnt >= 50 ? ' active' : '';
                    break;
                case 'onceAc_100':
                    classname += common.otherData.achievement.once_ac_cnt >= 100 ? ' active' : '';
                    break;
                case 'onceWa_10':
                    classname += common.otherData.achievement.once_wa_cnt >= 10 ? ' active' : '';
                    break;
                case 'onceWa_20':
                    classname += common.otherData.achievement.once_wa_cnt >= 20 ? ' active' : '';
                    break;
                case 'onceWa_50':
                    classname += common.otherData.achievement.once_wa_cnt >= 50 ? ' active' : '';
                    break;
                case 'onceWa_100':
                    classname += common.otherData.achievement.once_wa_cnt >= 100 ? ' active' : '';
                    break;
                case 'hasContestFirst':
                    classname += common.otherData.achievement.contest.is_first ? ' active' : '';
                    break;
                case 'hasContestLast':
                    classname += common.otherData.achievement.contest.is_last ? ' active' : '';
                    break;
                case 'valentine':
                    classname += common.otherData.achievement.festival.valentine ? ' active' : '';
                    break;
                case 'newyear':
                    classname += common.otherData.achievement.festival.newyear ? ' active' : '';
                    break;
                case 'single':
                    classname += common.otherData.achievement.festival.single ? ' active' : '';
                    break;
            }
            var template = `
                <li class="${classname}">
                    <span class="name">${achievementPageVar.achievements[key].title}</span>
                    <span class="desc">${achievementPageVar.achievements[key].desc}</span>
                    <span class="pic"></span>
                </li> 
            `;
            htmlStr += template;
        }
        achievementPageVar.dom.liWrap.html(htmlStr);
    }

    // 渲染 time-page
      function renderTimePage() {
        var ONEDAY = 86400000;
        var today = new Date().getTime();
        var lastday = common.indexData.last_submit_time;
        var between = '';
        var color = '';
        var colorInfo = ['#5DAC81', '#FFC408', '#CB1B45'];
        if (lastday === -1) {
            between = '∞';
            color = colorInfo[2];
        } else {
            between = Math.floor((today - lastday) / ONEDAY);
            if (between < 5) {
                color = colorInfo[0];
            } else if (between < 15) {
                color = colorInfo[1];
            } else {
                color = colorInfo[2];
            }
        }
        timePageVar.dom.dayText.html(between);
        timePageVar.dom.dayText.css('color', color);
    }


    // 调用渲染页面的函数
    function renderOtherPage() {
        renderFirstAcPage();
        renderLastAcPage();
        renderDifficultPage();
        renderContestPage();
        renderRankPage();
        renderAchievementPage();
        renderTimePage();
    }

    // logout
    function logout() {
        fnBarVar.dom.logout.on('click', function (e) {
            e.preventDefault();
            requestLogout();
        });
    }

    // 请求后台执行 logout 操作
    function requestLogout() {
        $.ajax({
            'type': 'GET',
            'data': '',
            'url': common.logoutURL,
            // 'dataType': 'json',
            // 'success': function () {
            //     console.log('logout');
            // }
        });
    }

    // reset
    function reset() {
        // 点击 reset 弹出交互弹层
        fnBarVar.dom.reset.on('click', function (e) {
            // 阻止 a 标签的默认事件
            e.preventDefault();
            fnBarVar.dom.alertWrap.css('display', 'block');
            fnBarVar.dom.alertBox.css('display', 'block');
            // 原密码项自动聚焦
            fnBarVar.dom.oldPas.focus();
            // 所有提示内容清空，因为点击取消时候，input 要响应提示的事件，又要响应退出的事件，所以在退出前提示事件可能还没有完成，所以如果把这个过程放在退出时完成不行
            fnBarVar.dom.oldPasHint.val('');
            fnBarVar.dom.newPasHint.val('');
            fnBarVar.dom.rePasHint.val('');
            fnBarVar.dom.oldPasHint.css('display', 'none');
            fnBarVar.dom.newPasHint.css('display', 'none');
            fnBarVar.dom.rePasHint.css('display', 'none');
            // 所有表单内容清空过，这个也不能放在点击取消事件时清空的原因是，弹层消失的方式不止点击取消一种，还有修改成功时的自动消失
            fnBarVar.dom.oldPas.val('');
            fnBarVar.dom.newPas.val('');
            fnBarVar.dom.newPasRe.val('');
        });

        // 点击 取消 隐藏 reset 交互层
        fnBarVar.dom.cancel.on('click', function () {
            // 所有表单原有值清空
            fnBarVar.dom.alertWrap.css('display', 'none');
        });

        // rePas 失去焦点时
        // 1. 提示不能为空
        // 2. 提示两次密码应该一致
        fnBarVar.dom.newPasRe
        .on('blur', function () {
            var newPas = fnBarVar.dom.newPas.val();
            var newPasRe = $(this).val();
            if (!newPasRe) {
                fnBarVar.dom.rePasHint.html(fnBarVar.newPasReHintText_2);
                fnBarVar.dom.rePasHint.css('display', 'block');
            } else if (newPas !== newPasRe) {
                // 密码不相同，提示用户
                fnBarVar.dom.rePasHint.html(fnBarVar.newPasReHintText_1);
                fnBarVar.dom.rePasHint.css('display', 'block');
                // 将另一处的密码不相同的提示关掉（因为另一处有可能有提示，有可能没有提示）
                fnBarVar.dom.newPasHint.html('');
                fnBarVar.dom.newPasHint.css('display', 'none');
            } else if (newPas === newPasRe) {
                // 密码相同后，把另一处有可能存在的错误提示关掉
                fnBarVar.dom.newPasHint.html('');
                fnBarVar.dom.newPasHint.css('display', 'none');
            }
        })
        .on('keyup', function (event) {
            // 给充值密码的 input 也就是最后一个 input 绑定 enter 事件，按下回车时也可提交
            if (event.keyCode == '13') {
                // 要先失去焦点，判断是否为空或者两次密码是否一致
                $(this).blur();
                handleBtn();
            }
        });

        // rePas 聚焦如果有错误提示就隐藏错误提示，并清空之前输入的内容
        fnBarVar.dom.newPasRe.on('focus', function () {
            if (fnBarVar.dom.rePasHint.css('display') === 'block') {
                $(this).val('');
                fnBarVar.dom.rePasHint.html('');
                fnBarVar.dom.rePasHint.css('display', 'none');
            }
        });

        // newPas 失去焦点时
        // 1. 提示不能为空
        // 2. 提示两次输入应该一致
        fnBarVar.dom.newPas.on('blur', function () {
            var newPas = $(this).val();
            var newPasRe = fnBarVar.dom.newPasRe.val();
            if (!newPas) {
                fnBarVar.dom.newPasHint.html(fnBarVar.newPasHintText_2);
                fnBarVar.dom.newPasHint.css('display', 'block');
            } else if (newPasRe && newPas !== newPasRe) {
                // 如果重复密码不为空，就检测两次密码是否一致，如果为空，可能用户还没有输入重复密码，所以不检测
                fnBarVar.dom.newPasHint.html(fnBarVar.newPasHintText_1);
                fnBarVar.dom.newPasHint.css('display', 'block');
                // 如果检测到两次密码不一致，则将重复密码的提示隐藏掉，因为如果这里也提示那里也提示，会出现两个密码不一致，用户不知道该改哪一个密码，所以原则就是在哪里出错，在哪里提示，把另一处的提示隐藏掉
                fnBarVar.dom.rePasHint.html('');
                fnBarVar.dom.rePasHint.css('display', 'none');
            } else if (newPasRe && newPas === newPasRe) {
                // 如果两次密码相等了，就把另一处的密码不一致的提示信息关掉
                fnBarVar.dom.rePasHint.html('');
                fnBarVar.dom.rePasHint.css('display', 'none');
            }
        });

        // newPas 聚焦时如果有错误提示就隐藏错误提示，并清空原油内容
        fnBarVar.dom.newPas.on('focus', function () {
            if (fnBarVar.dom.newPasHint.css('display') === 'block') {
                $(this).val('');
                fnBarVar.dom.newPasHint.html('');
                fnBarVar.dom.newPasHint.css('display', 'block');
            }
        });

        // oldPas 失去焦点时，检测是否为空
        fnBarVar.dom.oldPas.on('blur', function () {
            var oldPas = $(this).val();
            if (!oldPas) {
                fnBarVar.dom.oldPasHint.html(fnBarVar.oldPasHintText_2);
                fnBarVar.dom.oldPasHint.css('display', 'block');
            }
        });

        // oldPas 聚焦时，如果有错误提示就隐藏错误提示，并清空原有内容
        fnBarVar.dom.oldPas.on('focus', function () {
            // 如果有错误提示，清空原有内容，如果没有，则不请空
            if (fnBarVar.dom.oldPasHint.css('display') === 'block') {
                $(this).val('');
                fnBarVar.dom.oldPasHint.html('');
                fnBarVar.dom.oldPasHint.css('display', 'none');
            }
        });

        // 点击确定时
        fnBarVar.dom.confirmBtn.on('click', function () {
            handleBtn();
        });

        // 如果 input 都不为空，且密码一致才能请求
        function handleBtn() {
            var oldPas = fnBarVar.dom.oldPas.val(),
                newPas = fnBarVar.dom.newPas.val(),
                newPasRe = fnBarVar.dom.newPasRe.val(),
                oldPasHint = fnBarVar.dom.oldPasHint.css('display') === 'none' ? true : false,
                newPasHint = fnBarVar.dom.newPasHint.css('display') === 'none' ? true : false,
                rePasHint = fnBarVar.dom.rePasHint.css('display') === 'none' ? true : false;
            if (oldPas && newPas && newPasRe && oldPasHint && newPasHint && rePasHint) {
                requestResetPas(oldPas, newPas);
            }
        }

        // 发送 reset 请求
        function requestResetPas(oldPas, newPas) {
            $.ajax({
                'type': 'POST',
                'data': `password_old=${oldPas}&password_new=${newPas}`,
                'url': common.resetURL,
                'dataType': 'text',
                'success': function (data) {
                    resetCb(data);
                }
            });
        }

        // 响应 reset 请求
        function resetCb(data) {
            // data = 0;
            if (data === '0') {
                fnBarVar.dom.alertBox.fadeOut(500);
                fnBarVar.dom.correct.fadeIn(500).delay(1200).fadeOut(500, function () {
                    fnBarVar.dom.alertWrap.fadeOut(500);
                });
            } else {
                fnBarVar.dom.oldPasHint.html(fnBarVar.oldPasHintText_1);
                fnBarVar.dom.oldPasHint.css('display', 'block');
            }
        }

    }

    init();
})();
