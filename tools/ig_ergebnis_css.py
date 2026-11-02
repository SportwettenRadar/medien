"""CSS-Bausteine der Ergebnis-Beiträge (aus den freigegebenen Beispielen, 02.11.2026)."""
BASE = """
.tag{position:absolute;left:88px;bottom:150px;font-family:M;font-size:24px;color:#0a1620;background:#f2c14e;padding:8px 18px;border-radius:12px;letter-spacing:.08em}
.row{display:flex;align-items:center;justify-content:space-between;background:#0f1d2c;border:2px solid #1b2c40;border-radius:26px;padding:22px 32px;margin-top:18px}
.row .t{font-size:33px;line-height:1.25;color:#eef3f8}.row .t small{display:block;font-size:26px;color:#8aa0b5;margin-top:4px}
.ok,.no{flex:none;font-family:B;font-weight:800;font-size:30px;padding:10px 24px;border-radius:40px;margin-left:20px}
.ok{background:#2edb99;color:#0a1620}.no{background:#26364a;color:#c9d6e3;border:2px solid #3a4f68}
.d{display:flex;align-items:center;justify-content:space-between;margin-top:18px;background:#0f1d2c;border:2px solid #1b2c40;border-radius:26px;padding:20px 32px}
.d b{font-family:B;font-weight:800;font-size:36px;width:90px}
.dots{display:flex;gap:12px;flex-wrap:wrap;justify-content:flex-end;flex:1}
.dots i{width:34px;height:34px;border-radius:50%;background:#2edb99}.dots i.l{background:#26364a;border:2px solid #3a4f68}
.main.t h1{font-size:60px}.main.t .row{padding:14px 28px;margin-top:12px;border-radius:22px}.main.t .row .t{font-size:30px}.main.t .row .t small{font-size:24px}.main.t .ok,.main.t .no{font-size:27px;padding:8px 20px}.main.t .d{padding:12px 26px;margin-top:11px;border-radius:22px}.main.t .d b{font-size:32px}.main.t .dots i{width:28px;height:28px}.main.t .sub{font-size:30px;margin-top:18px}.main.t .leg{margin-top:18px}
.leg{display:flex;gap:34px;margin-top:26px;font-size:28px;color:#a9b8c8;align-items:center}
.leg i{display:inline-block;width:26px;height:26px;border-radius:50%;background:#2edb99;margin-right:12px;vertical-align:-4px}.leg i.l{background:#26364a;border:2px solid #3a4f68}
"""
TAB = """
.tag{left:88px;right:auto;bottom:auto;top:228px}
.tb{position:absolute;left:88px;right:88px;top:352px}
.th{display:flex;font-family:M;font-size:21px;letter-spacing:.14em;color:#6f8399;padding:0 22px 8px}
.th span:nth-child(1){width:52px}.th span:nth-child(2){flex:1}.th span:nth-child(3){width:110px}.th span:nth-child(4){width:100px;text-align:right}.th span:nth-child(5){width:70px}
.tr{display:flex;align-items:center;height:56px;margin-top:5px;background:#0f1d2c;border:2px solid #1b2c40;border-radius:16px;padding:0 22px;font-size:27px;color:#eef3f8}
.tr em{font-style:normal;font-family:M;font-size:22px;color:#6f8399;width:52px}
.tr div{flex:1;white-space:nowrap;overflow:hidden}
.tr span{font-family:M;font-size:24px;color:#a9b8c8;width:110px}
.tr b{font-family:M;font-weight:500;font-size:26px;width:100px;text-align:right}
.tr u{text-decoration:none;width:44px;height:44px;margin-left:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:B;font-weight:800;font-size:28px}
.tr u.w{background:#2edb99;color:#0a1620}.tr u.l{background:#26364a;color:#c9d6e3;border:2px solid #3a4f68}
.big .th{font-size:24px;padding:0 30px 12px}.big .th span:nth-child(1){width:64px}.big .th span:nth-child(3){width:140px}.big .th span:nth-child(4){width:120px}.big .th span:nth-child(5){width:90px}
.big .tr{height:104px;margin-top:10px;border-radius:24px;padding:0 30px;font-size:34px}.big .tr em{font-size:28px;width:64px}.big .tr span{font-size:28px;width:130px}
.big .tr b{font-size:34px;width:120px}.big .tr u{width:56px;height:56px;font-size:38px;margin-left:30px}
.big .leg{margin-top:24px;font-size:28px}.big .leg u{width:36px;height:36px;font-size:22px}.big .note{font-size:32px;margin-top:24px}
.leg{display:flex;gap:34px;margin-top:20px;font-size:25px;color:#a9b8c8;align-items:center}
.leg u{display:inline-flex;width:30px;height:30px;border-radius:50%;text-decoration:none;align-items:center;justify-content:center;font-size:19px;font-weight:800;margin-right:10px;background:#2edb99;color:#0a1620}.leg u.l{background:#26364a;color:#c9d6e3;border:2px solid #3a4f68}
.note{font-size:30px;line-height:1.4;color:#a9b8c8;margin-top:30px}
"""
WOCHE = """
.tag{left:88px;right:auto;bottom:auto;top:228px}
.tb{position:absolute;left:88px;right:88px;top:360px}
.wr{display:flex;align-items:flex-start;background:#0f1d2c;border:2px solid #1b2c40;border-radius:20px;padding:16px 24px;margin-top:10px}
.wr b{font-family:B;font-weight:800;font-size:30px;width:150px;flex:none;line-height:34px}
.wr b small{display:block;font-family:M;font-weight:400;font-size:20px;color:#6f8399;line-height:22px}
.dt{display:flex;flex-wrap:wrap;gap:8px;flex:1;align-content:flex-start;min-height:34px}
.dt i{width:30px;height:30px;border-radius:50%;background:#2edb99}.dt i.l{background:#26364a;border:2px solid #3a4f68}
.m .dt i{width:24px;height:24px}.m .dt{gap:7px}.m .wr b{width:190px}
.leg{display:flex;gap:34px;margin-top:22px;font-size:26px;color:#a9b8c8;align-items:center}
.leg i{display:inline-block;width:26px;height:26px;border-radius:50%;background:#2edb99;margin-right:12px;vertical-align:-4px}.leg i.l{background:#26364a;border:2px solid #3a4f68}
.big .wr{padding:20px 28px;margin-top:10px;border-radius:24px}
.big .wr b{font-size:36px;width:170px;line-height:40px}.big .wr b small{font-size:22px;line-height:26px;margin-top:2px}
.big .wr{align-items:center}.big .dt{gap:16px;align-items:center}.big .dt i{width:42px;height:42px}
.big.m .dt{gap:10px}.big.m .dt i{width:36px;height:36px}.big.m .wr{padding:34px 28px}
.big.w2 .wr{padding:13px 28px;margin-top:8px}.big .leg{margin-top:22px;font-size:28px}.big .note{font-size:32px;margin-top:22px}
.note{font-size:30px;line-height:1.4;color:#a9b8c8;margin-top:26px}
"""
