import json
import difflib
from bottle import route, run, request, abort


tatort_json = 'tatort.json'

with open('tatort.json') as f:
    data = json.load(f)


@route('/nummer/:episoden_nummer', method='GET')
def nummer(episoden_nummer):
    for i in data:
        if episoden_nummer == i['nummer']:
            return i

    abort(404, '%s nicht gefunden' % episoden_nummer)


@route('/darsteller/:name', method='GET')
def darsteller(name):
    episoden_list = []
    for i in data:
        if name in i['darsteller']:
            episoden_list.append(i['nummer'])

    if len(episoden_list) > 0:
        return {'nummer': episoden_list}
    else:
        darsteller_list = []
        for i in data:
            for j in i['darsteller']:
                darsteller_list.append(j.strip())

        darsteller_list = list(set(darsteller_list))
        close_darsteller = difflib.get_close_matches(name, darsteller_list)
        close_darsteller = ', '.join(close_darsteller)
        if len(close_darsteller) > 0:
            abort(404, '"%s" nicht gefunden. Meinten sie: %s?'
                  % (name, close_darsteller))
        else:
            abort(404, '"%s" nicht gefunden' % name)


@route('/titel/:name', method='GET')
def titel(name):
    titel_list = []
    for i in data:
        if name == i['titel']:
            return i

        titel_list.append(i['titel'])

    titel_list = list(set(titel_list))
    close_titel = difflib.get_close_matches(name, titel_list)
    close_titel = ', '.join(close_titel)
    if len(close_titel) > 0:
        abort(404, '"%s" nicht gefunden. Meinten sie: %s?'
              % (name, close_titel))
    else:
        abort(404, '"%s" nicht gefunden' % name)


if __name__ == '__main__':
    run(debug=True)
