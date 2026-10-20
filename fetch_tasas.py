import os, json, sys, time, datetime as dt, urllib.request, urllib.parse
T = os.environ.get('TOKEN', '').strip()
if not T:
    sys.exit('Falta el secreto ELTOQUE_TOKEN en GitHub.')
try:
    H = json.load(open('tasas.json'))
except Exception:
    H = {}
def get(d):
    q = urllib.parse.urlencode({'date_from': d + ' 00:00:01', 'date_to': d + ' 23:59:01'})
    r = urllib.request.Request('https://tasas.eltoque.com/v1/trmi?' + q,
        headers={'Authorization': 'Bearer ' + T, 'Accept': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=30)).get('tasas', {})
hoy = dt.date.today(); ok = 0; fallos = 0
for n in range(30, -1, -1):
    d = str(hoy - dt.timedelta(days=n))
    if d in H and n > 0:
        continue
    try:
        t = get(d); out = {}
        for k, c in (('USD', 'USD'), ('ECU', 'EUR'), ('EUR', 'EUR'), ('MLC', 'MLC')):
            if t.get(k):
                out[c] = float(t[k])
        if out:
            H[d] = out; ok += 1
        print(d, out or 'sin datos', t if not out else '')
    except Exception as e:
        fallos += 1; print(d, 'ERROR', e)
    time.sleep(0.5)
json.dump(dict(sorted(H.items())), open('tasas.json', 'w'), indent=0)
print('Dias guardados:', ok, 'Errores:', fallos)
if ok == 0 and fallos:
    sys.exit(1)
