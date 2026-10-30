# Outlander SDA – DAB+ preset steering-wheel controls

Cílem projektu je nejprve **analyzovat** firmware jednotky Mitsubishi Outlander SDA (modelový rok 2017) a zjistit, jak bezpečně změnit chování tlačítek na volantu při poslechu DAB+.

## Požadované chování

- Krátký stisk levé/pravé šipky přepíná uložené DAB+ předvolby.
- Předvolby se procházejí napříč třemi bankami (celkem až 18 pozicemi).
- Prázdné pozice se pokud možno přeskočí.
- Po dosažení konce seznamu se přepínání případně vrátí na začátek.
- Šipky nahoru/dolů pro hlasitost zůstanou beze změny.
- FM/AM není v první fázi cílem; priorita je DAB+.

## Bezpečnostní pravidla

Tento repozitář je určen pro **analýzu a přípravu**, nikoli pro okamžité flashování rádia.

1. Originální firmware vždy uchovávat beze změny a pracovat s kopií.
2. Neprovádět zápis do jednotky, dokud nebude známá přesná změna, způsob ověření a realistická možnost obnovy.
3. Nepublikovat firmware ani extrahované proprietární soubory.
4. Každý závěr ověřit v kódu; samotné nalezení názvu funkce nebo řetězce není důkazem jejího chování.

## Dosavadní výchozí poznatky

Předběžná analýza dříve identifikovala v balíčku aplikace názvy související s obsluhou hardwarových tlačítek, DAB skipem a změnou předvolby. Tyto indicie je nutné znovu ověřit proti konkrétnímu obrazu firmwaru a návaznosti volání.

## Struktura

- `tools/inspect_nfu.py` – bezpečná inventarizace vnitřního ZIP archivu souboru NFU; volitelně vyextrahuje pouze `system.img`.
- `.github/workflows/python-checks.yml` – kontrola syntaxe pomocného skriptu.

## Použití analyzátoru

Vyžaduje Python 3.10+ a původní soubor NFU, který zůstává mimo Git:

```bash
python tools/inspect_nfu.py cesta/k/firmware.nfu
python tools/inspect_nfu.py cesta/k/firmware.nfu --extract-system /bezpecna/pracovni/slozka
```

Skript pouze čte vstupní firmware. Neprovádí žádné změny ani zápis do rádia.
