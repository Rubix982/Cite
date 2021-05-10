# Proxii

## Pipenv

Using `Pipenv`,

```bash
pipenv shell
```

Updating `Pipfile`,

```bash
pipenv install -r requirements.txt
```

Updating `Pipfile.lock`,

```bash
pipenv lock --pre --clear
```

Installing a package,

```bash
pipenv install [package_name]
```

## Application

Starting the proxy server,

```bash
python3 app.py
```

## OpenSSL

Generating new self signed certificates,

```bash
openssl req -new -x509 -days 365 -nodes -out certificate.pem -keyout private_key.pem
```

## HTTP websites

List of websites that still use HTTP. For demonstration purposes only,

- baidu.com
- sohu.com
- xinhuanet.com
- apache.org
- w3.org
- babytree.com
- myshopify.com
- whitepages.com
- tianya.cn
- go.com
- mit.edu
- gnu.org
- panda.tv
- soso.com
- china.com.cn
- hugedomains.com
- rednet.cn
- nature.com
- drudgereport.com
- nginx.org
- techcrunch.com
- moatads.com
- miit.gov.cn
- beian.gov.cn
- 17ok.com
- washington.edu
- thestartmagazine.com
- jrj.com.cn
- rlcdn.com
- definition.org
- brainly.com
- ntp.org
- chinadaily.com.cn
- tripod.com
- tapad.com
- axs.com
- yimg.com
- startribune.com
- cbc.ca
- geocities.com
- gmw.cn
- eastday.com
- eepurl.com
- cafemom.com
- ucla.edu
- hdfcbank.com
- example.com
- gohoi.com
- techofires.com
- www.gov.cn
- ox.ac.uk
- sigonews.com
- lenovo.com
- itfactly.com
- aboutads.info
- reverso.net
- ideapuls.com
- sendgrid.net
- genius.com
- easybib.com
- nyu.edu
- shareasale-analytics.com
- bizrate.com
- redfin.com
- ufl.edu
- icio.us
- cowner.net
- oecd.org
- youth.cn
- cctv.com
- theconversation.com
- trend-chaser.com
- imageshack.us
- youdao.com
- fao.org
- angelfire.com
- chinanews.com
- hexun.com
- youronlinechoices.com
- tencent.com
- lijit.com
- dedecms.com
- senate.gov
- zol.com.cn
- 51sole.com
- bu.edu
- livedoor.jp
- adoptapet.com
- rutgers.edu
- ihg.com
- dmm.co.jp
- medicinenet.com
- zemanta.com
- wikidot.com
- tremorhub.com
- dmoz.org
- cntv.cn
- zara.com
- alternativenation.net
- namnak.com

## References

- [Docs Python, OpenSSL - Self-signed Certificates](https://docs.python.org/3.6/library/ssl.html#self-signed-certificates)
- [WhyNoHTTPS](https://whynohttps.com/)
