import os.path
import random
import re
import time
from datetime import datetime, timedelta
import pytest
from py.xml import html
from PIL import ImageGrab, Image


plt = ...  # plt: pyplot对象，需要在外层import matplotlib.pyplot as plt，然后指定plt
INDEX_URL = ...
USER_NAME = ...
PASSWORD = ...
SYS_NAME = ...
AUTO_OPEN = False
BASE_PATH = os.path.split(os.path.abspath(__file__))[0]

# 下面的不用指定了
_OUTPUT_DIR = os.path.join(BASE_PATH, "Outputs")
_REPORT_PATH = os.path.join(_OUTPUT_DIR, "report")
_HTML_REPORT_PATH = os.path.join(_REPORT_PATH, "report.html")
_SUMMARY_PIC_PATH = os.path.join(_REPORT_PATH, "summary.jpg")
_LOG_DIR = os.path.join(_OUTPUT_DIR, "logs")
_SCREENSHOT_DIR = os.path.join(_REPORT_PATH, "screenshots")
for _ in [_REPORT_PATH, _SCREENSHOT_DIR, _LOG_DIR]:
    if not os.path.exists(_):
        os.makedirs(_)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == 'setup':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            if file_name:
                screen_img = _screenshot_()
                html_ = (
                        '<div><img src="%s" alt="screenshot" style="width:469px;height:240px;" '
                        'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                )
                extra.append(pytest_html.extras.html(html_))
    doc = str(item.function.__doc__)
    if len(doc) > 120:
        doc = doc[:120] + '...'
    report.description = doc
    report.extra = extra


def pytest_html_results_table_row(report, cells):
    try:
        cells.insert(2, html.td(report.description))
    except AttributeError:
        ...
    cells.insert(3, html.td(time.strftime('%Y-%m-%d %H:%M:%S'), class_='col-time'))
    cells.pop()
    for i in range(len(cells)):
        cells[i].attr.__setattr__('style', 'border:1.4px solid #%s' % _color)


def pytest_html_results_table_header(cells):
    cells[0].attr.width = '200px'
    cells[1].attr.width = '500px'
    cells.insert(2, html.th("Description", width='720px'))
    cells.insert(3, html.th("Time", class_="sortable time", col="time", width='335px'))
    cells[4].attr.width = '130px'
    cells.pop()
    for i in range(len(cells)):
        cells[i].attr.__setattr__('style', 'border:2.8px solid #%s' % _color_())


def pytest_html_report_title(report):
    report.title = 'Test Report'


def pytest_html_results_summary(prefix):
    prefix.extend([html.div(html.img(
        src=r'./summary.jpg', alt='Summary'),
        style="width:0px;height:125px;margin:-140px 0px 0px 920px"
    )])


def pytest_sessionfinish(session):
    reporter = session.config.pluginmanager.get_plugin('terminalreporter')
    reporter_stats = reporter.stats
    p = _get_pfs_(reporter_stats, 'passed')
    f = _get_pfs_(reporter_stats, 'failed')
    s = _get_pfs_(reporter_stats, 'skipped')

    _clear_(_SCREENSHOT_DIR)
    _clear_(_LOG_DIR)
    _draw_(p, f, s)
    _html_sub_()


__color__ = ['32cd99', '7093db', 'db7093', '236b8e', 'cc3299', '8fbc8f', 'b4eeb4']  # 表头颜色-好看
_color = random.choice(['ffccff', 'ccccff', '99ccff'])  # 表单颜色-更淡


def _color_():
    _ = random.choice(__color__)
    if len(__color__) > 1:
        __color__.remove(_)
    return _


def _get_pfs_(reporter_stats, type_):
    try:
        nb = len(reporter_stats[type_])
    except KeyError:
        nb = 0
    return nb


def _clear_(dir_path):
    files = os.listdir(dir_path)
    files_date = [(file, datetime.fromtimestamp(os.stat(os.path.join(dir_path, file)).st_ctime)) for file in files]
    sorted_file = [(os.path.join(dir_path, x[0]), x[1]) for x in sorted(files_date, key=lambda x: x[1], reverse=True)]
    for i in sorted_file:
        file, date = i
        if date < datetime.today() - timedelta(days=4):
            os.remove(file)


def _html_sub_():
    with open(_HTML_REPORT_PATH, 'r', encoding='utf-8') as f:
        con = f.read()
    res = re.sub('<p>Report generated.*</p>', '', con)
    password = PASSWORD or '空'
    link = f'<div style="height:26px; color:green">Test Url : <a href={INDEX_URL} style="color:green">' \
           f'{INDEX_URL}</a></div>' \
           f'<div style="height:30px; color:green">Test By : name: {USER_NAME} &nbsp|&nbsp password: {password}' \
           f' &nbsp|&nbsp 名称: {SYS_NAME}</div>'
    res = re.sub('<h2>Summary</h2>', link, res)
    with open(_HTML_REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(res)
    if AUTO_OPEN:
        import webbrowser
        webbrowser.open(_HTML_REPORT_PATH)


def _screenshot_():
    file_name = datetime.now().strftime('%Y%m%d%H%M%S%f') + '.png'
    file_path = os.path.join(_SCREENSHOT_DIR, file_name)
    ImageGrab.grab(bbox=(0, 0, 1920, 1080)).save(file_path)
    file_path = './screenshots/' + file_name
    return file_path


def _draw_(p, f, s):
    if plt is ...:
        return
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    sm = p + f + s
    if not sm:
        return
    x = [p / sm, f / sm]
    labels = ['Pass', 'Fail']
    if s / sm:
        x.append(s / sm)
        labels.append('Skip')

    plt.figure(figsize=(3.3, 3.3))
    plt.pie(
        x=x,
        # labels=labels,
        # labeldistance=1.05,
        autopct='%.2f%%',
        pctdistance=1.33,
        textprops={'fontsize': 10},
        # colors=['r', 'g', 'y'],
        wedgeprops={'width': 0.35},
        startangle=10
    )
    legend_labels = [f'Pass {p}/{sm}', f'Fail {f}/{sm}']
    if s / sm:
        legend_labels.append(f'Skip {s}/{sm}')
    plt.legend(legend_labels, loc='upper left', bbox_to_anchor=(0.98, 0.93), fontsize=9)
    plt.title('Summary Chart', fontsize=11, loc='center')
    plt.tight_layout()
    plt.savefig(_SUMMARY_PIC_PATH)

    img = Image.open(_SUMMARY_PIC_PATH)
    c_img = img.crop((0, 10, img.width, img.height - 45))
    c_img.save(_SUMMARY_PIC_PATH)

# def pytest_collection_modifyitems(items):
#     for item in items:
# item.name = item.name.encode('UTF-8').decode('unicode-escape')
# item.name = item.name.encode('unicode-escape').decode('UTF-8')
# item._nodeid = item._nodeid.encode('unicode-escape').decode('UTF-8')
# item._nodeid = item._nodeid.encode('UTF-8').decode('unicode-escape')
