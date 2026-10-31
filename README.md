# Outlander SDA – DAB+ preset steering-wheel controls

Cílem projektu je analyzovat firmware jednotky Mitsubishi Outlander SDA (modelový rok 2017) a připravit bezpečnou změnu chování tlačítek na volantu při poslechu DAB+.

## Požadované chování

- Krátký stisk levé/pravé šipky přepíná uložené DAB+ předvolby.
- Předvolby se procházejí napříč třemi bankami (celkem až 18 pozicemi).
- Prázdné pozice se přeskočí.
- Po dosažení konce se přepínání vrátí na začátek a opačně.
- Šipky nahoru/dolů pro hlasitost zůstanou beze změny.
- FM/AM není v první fázi cílem; priorita je DAB+.

## Bezpečnost

Tento repozitář je určen pro analýzu a přípravu, nikoli pro okamžité flashování rádia.

1. Originální firmware vždy uchovávat beze změny a pracovat s kopií.
2. Neprovádět zápis do jednotky, dokud nebude známá přesná změna, způsob ověření a realistická možnost obnovy.
3. Nepublikovat firmware ani extrahované proprietární soubory.
4. Každý závěr ověřit v bytekódu; samotné názvy funkcí nejsou důkazem jejich chování.
5. První workflow pouze rozebírá APK. Nic nepodepisuje, neupravuje ani neinstaluje.

## Analýza firmwaru

- `tools/inspect_nfu.py` – read-only inventarizace NFU a volitelná extrakce `system.img`.
- `.github/workflows/python-checks.yml` – kontrola syntaxe pomocného skriptu.
- `.github/workflows/inspect-sda-apk.yml` – read-only rozložení DEX do Smali přes Baksmali a vytvoření artefaktu pro kontrolu metod.

### Co je potřeba dodat pro analýzu APK

Workflow očekává původní `GuiApp.apk`. Protože GitHub web nepřijme soubor této velikosti v jednom kuse, použij dva části:

1. Zkontroluj, že repozitář `kakaovyjoe/outlander-sda-dab-preset` je **Private**.
2. Vytvoř v repozitáři složku `work` (například **Add file → Create new file**, název `work/.gitkeep`, potom commit).
3. Otevři složku `work` a přes **Add file → Upload files** nahraj oba soubory `GuiApp.apk.part1` a `GuiApp.apk.part2`.
4. Potvrď commit do větve `main`. Workflow je automaticky spojí ve správném pořadí, ověří SHA-256 a provede kontrolu APK.
5. Po dokončení otevři běh workflow → **Artifacts** → `outlander-sda-smali-analysis` a stáhni ZIP. Pro další práci budou potřeba zejména soubory tříd `EntDabLibrary`, `EntDabModel`, `EntDabPresetController` a `EntDabPresetList`.

**Upozornění k soukromí:** nahráním obou částí se binární obsah APK uloží do historie tohoto Git repozitáře. I když je repozitář soukromý, dělej to pouze tehdy, pokud s tím souhlasíš. Po analýze lze naplánovat odstranění souborů z aktuální větve, ale odstranění commitu samo o sobě nevymaže starší historii.

Workflow vyžaduje přístup k Maven Central pro stažení Baksmali. Výstupní artefakt je dočasný (7 dní). Tento krok nic nemění na rádiu.

## Analýza NFU lokálně

Vyžaduje Python 3.10+ a původní soubor NFU, který zůstává mimo Git:

```bash
python tools/inspect_nfu.py cesta/k/firmware.nfu
python tools/inspect_nfu.py cesta/k/firmware.nfu --extract-system /bezpecna/pracovni/slozka
```

## Stav úpravy DAB tlačítek na volantu (31. 10. 2026)

- Byla připravena a úspěšně zkompilována změna krátkého stisku hardwarových šipek DAB: vpřed/vzad prochází obsazené uložené předvolby 1–18, přeskakuje prázdné pozice a obíhá mezi začátkem a koncem.
- Ovládání vyhledávání na obrazovce zůstává beze změny. Dlouhé podržení / opakované hledání také zůstává původní. Hlasitost není součástí upravované DAB knihovny.
- GitHub Actions úspěšně sestavil kontrolní DEX a přebalený APK archiv. Výsledek je zatím **nepodepsaný validační náhled**, nikoli soubor k instalaci.
- Původní APK obsahuje pouze veřejná data podpisového certifikátu Android Debug; privátní podpisový klíč ve firmwaru ani APK není. Modifikovaný APK proto nelze bezpečně nainstalovat jako aktualizaci původní aplikace.
- **Neinstalovat a neflashovat** validační APK. Před jakýmkoli testem v jednotce je nutné vyřešit kompatibilní podpis/aktualizační cestu a ověřenou obnovu jednotky.

Podrobnosti: [reports/dab-patch-validation.md](reports/dab-patch-validation.md). Výsledek GitHub Actions: https://github.com/kakaovyjoe/outlander-sda-dab-preset/actions/runs/41194937933.
