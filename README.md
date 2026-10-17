[Português](#português) · [English](#english)

# Português

**Um tema de cursores inspirado no macOS para desktops Linux, com cursores SVG escaláveis para GNOME 51 e KDE Plasma 6.2+.**

Este *fork* dá continuidade ao projeto [yeyushengfan258/Future-cursors](https://github.com/yeyushengfan258/Future-cursors), um tema de cursores inspirado no macOS e baseado no [Capitaine Cursors](https://github.com/keeferrourke/capitaine-cursors). Ele preserva a geração dos arquivos Xcursor tradicionais e acrescenta os cursores SVG escaláveis, além de scripts para compilar e instalar as variantes padrão e Cyan.

> **Estado do projeto:** Os scripts de compilação e instalação foram executados com sucesso em um ambiente Arch Linux nos testes iniciais. A aparência e o comportamento dos cursores no GNOME 51 ainda estão sendo verificados; nem todos os ambientes gráficos, aplicativos e estados de cursor foram validados.

## Prévia

![Prévia do Future Cursors](preview.png)

![Prévia adicional do Future Cursors](preview-1.png)

## Variantes

| Tema | Diretório SVG de origem | Saída da compilação | Diretório instalado | Nome exibido |
|---|---|---|---|---|
| Padrão | `src/svg/` | `dist/` | `Future-cursors/` | **Future Cursors** |
| Cyan | `src/svg-cyan/` | `dist-cyan/` | `Future-cursors-cyan/` | **Future Cursors Cyan** |

Cada variante é compilada separadamente e inclui duas representações dos cursores:

- `cursors/` — arquivos Xcursor tradicionais, mantidos para compatibilidade com aplicativos antigos e ambientes que não utilizam cursores SVG escaláveis.
- `cursors_scalable/` — arquivos SVG e seus respectivos `metadata.json`, para ambientes gráficos compatíveis com o formato escalável.

Os metadados SVG são gerados a partir dos arquivos de configuração de cursores já existentes, preservando as coordenadas do ponto de ativação (*hotspot*), o tamanho nominal e o intervalo entre quadros de animações, quando especificados. Os aliases são gerados a partir de `src/cursorList`; o script também tenta fornecer os nomes `all-resize` e `dnd-ask`, esperados pelo protocolo de formas de cursor utilizado pelo GNOME. Os dois temas definem o Adwaita como fallback por meio do `index.theme`.

## Dependências

Os scripts precisam de Bash, Python 3, Inkscape e `xcursorgen`, além dos utilitários de linha de comando normalmente disponíveis no sistema.

No Arch Linux:

```bash
sudo pacman -S inkscape xorg-xcursorgen python
```

Em outras distribuições, instale os pacotes equivalentes pelo gerenciador de pacotes utilizado.

## Compilar as duas variantes

Execute os comandos a partir da raiz do repositório:

```bash
chmod +x build-gnome51.sh install-gnome51.sh
./build-gnome51.sh
```

O script de compilação:

1. Executa o `build.sh` original para gerar a variante Xcursor padrão.
2. Gera `cursors_scalable/` e os metadados SVG a partir de `src/svg/`.
3. Compila a variante Cyan em uma cópia temporária e isolada da árvore de fontes, impedindo que os PNGs intermediários e os arquivos Xcursor dessa variante sobrescrevam os da versão padrão.
4. Gera os cursores SVG Cyan e salva o tema final em `dist-cyan/`.

Ao final de uma compilação bem-sucedida, as pastas `dist/` e `dist-cyan/` devem conter `index.theme`, `cursors/` e `cursors_scalable/`.

O comando original `./build.sh` continua disponível caso você queira gerar apenas o tema Xcursor tradicional. O `./install.sh` original instala somente a variante padrão; para instalar as duas, use `install-gnome51.sh`.

## Instalação

### Instalar apenas para o usuário atual (recomendado)

```bash
./install-gnome51.sh
```

Os temas serão instalados em `${XDG_DATA_HOME:-$HOME/.local/share}/icons/`.

### Instalar para todos os usuários

```bash
sudo ./install-gnome51.sh
```

Os temas serão instalados em `/usr/share/icons/`. O instalador substitui as cópias já existentes de `Future-cursors` e `Future-cursors-cyan` no destino selecionado.

Depois da instalação, abra o GNOME Tweaks ou as configurações de cursores do ambiente gráfico e selecione **Future Cursors** ou **Future Cursors Cyan**. Se o desktop continuar mostrando arquivos em cache, pode ser necessário selecionar o tema novamente ou reiniciar a sessão.

## Avisos conhecidos e estado dos testes

Durante as compilações iniciais com o Inkscape, foram observados estes avisos:

- `Duplicate option text ('Eixo X')`, emitido pela extensão `org.inkscape.render.poly_3d`.
- `Ignoring unrecognized CSS property: block-progression`.

Esses avisos não impediram a conclusão da compilação e da instalação no ambiente testado. Até o momento, não foi estabelecido que eles causem erros na renderização dos cursores. Ainda assim, confira o código de saída e verifique se as duas pastas de saída contêm os arquivos esperados; não ignore erros de compilação distintos apenas por aparecerem junto desses avisos.

O comportamento visual de todos os formatos de cursor, pontos de ativação, animações e variantes de cor continua em fase de testes. Ao relatar um cursor ausente, desalinhado ou exibido incorretamente, informe o ambiente gráfico e sua versão, a variante selecionada e o nome do cursor afetado.

## Créditos e licença

- **Tema original Future Cursors:** [yeyushengfan258/Future-cursors](https://github.com/yeyushengfan258/Future-cursors).
- **Base do design:** [Capitaine Cursors](https://github.com/keeferrourke/capitaine-cursors), conforme os créditos do projeto original.
- **Informações sobre o formato de cursores SVG:** [KDE: SVG cursors — everything that you need to know about them](https://planet.kde.org/vlad-zahorodnii-2024-10-06-svg-cursors-everything-that-you-need-to-know-about-them/).

O repositório original identifica o projeto sob a licença **GPL-3.0**. Mantenha o arquivo `LICENSE` do repositório neste *fork* e consulte-o para conhecer os termos aplicáveis. Os scripts de compilação e instalação deste *fork* são acréscimos ao projeto original e não substituem os créditos da arte original.

----

# Future Cursors

**A macOS-inspired cursor theme for Linux desktops, with scalable SVG cursors for GNOME 51 and KDE Plasma 6.2+.**

# English

This fork builds on [yeyushengfan258/Future-cursors](https://github.com/yeyushengfan258/Future-cursors), a cursor theme inspired by macOS and based on [Capitaine Cursors](https://github.com/keeferrourke/capitaine-cursors). It keeps the original Xcursor output and adds scalable SVG cursor data, plus build and installation support for both the default and Cyan variants.

> **Project status:** The build and installation scripts completed successfully in an Arch Linux environment during initial testing. The cursor appearance and behavior in GNOME 51 are still being checked; not every desktop, application, or cursor state has been validated yet.

## Preview

![Future Cursors preview](preview.png)

![Future Cursors additional preview](preview-1.png)

## Variants

| Theme | Source SVG directory | Build output | Installed theme directory | Display name |
|---|---|---|---|---|
| Default | `src/svg/` | `dist/` | `Future-cursors/` | **Future Cursors** |
| Cyan | `src/svg-cyan/` | `dist-cyan/` | `Future-cursors-cyan/` | **Future Cursors Cyan** |

Each variant is built separately and includes two cursor representations:

- `cursors/` — traditional Xcursor files, retained for compatibility with older applications and environments that do not use scalable SVG cursors.
- `cursors_scalable/` — SVG cursor files and `metadata.json` files for desktops that support the scalable cursor format.

The SVG metadata is generated from the existing cursor configuration files, preserving each frame's hotspot coordinates, nominal size, and animation delay where specified. Cursor aliases are generated from `src/cursorList`; the builder also attempts to provide the `all-resize` and `dnd-ask` names expected by GNOME's cursor-shape protocol. Both themes set Adwaita as their fallback through `index.theme`.

## Requirements

The scripts require Bash, Python 3, Inkscape, and `xcursorgen`, in addition to standard command-line utilities.

On Arch Linux:

```bash
sudo pacman -S inkscape xorg-xcursorgen python
```

On other distributions, install the equivalent packages using your package manager.

## Build both variants

Run these commands from the repository root:

```bash
chmod +x build-gnome51.sh install-gnome51.sh
./build-gnome51.sh
```

The build script:

1. Runs the original `build.sh` to generate the default Xcursor theme.
2. Generates `cursors_scalable/` and SVG metadata for `src/svg/`.
3. Builds the Cyan variant from an isolated temporary copy of the source tree, so its intermediate PNG files and Xcursor output do not overwrite the default variant.
4. Generates the Cyan SVG cursor data and writes the completed theme to `dist-cyan/`.

Successful output should leave both `dist/` and `dist-cyan/` with an `index.theme`, a `cursors/` directory, and a `cursors_scalable/` directory.

The original `./build.sh` remains available if you only need the original Xcursor build. The original `./install.sh` installs only the default theme; use `install-gnome51.sh` to install both variants.

## Install the themes

### Install for the current user (recommended)

```bash
./install-gnome51.sh
```

The themes are installed to `${XDG_DATA_HOME:-$HOME/.local/share}/icons/`.

### Install system-wide

```bash
sudo ./install-gnome51.sh
```

The themes are installed to `/usr/share/icons/`. The installation script replaces existing installed copies of `Future-cursors` and `Future-cursors-cyan` in the selected destination.

After installation, open GNOME Tweaks or your desktop environment's cursor settings and select **Future Cursors** or **Future Cursors Cyan**. You may need to reselect the theme or restart the session if the desktop continues to display cached cursor assets.

## Known warnings and testing notes

During initial builds with Inkscape, the following warnings were observed:

- `Duplicate option text ('Eixo X')` from the `org.inkscape.render.poly_3d` extension.
- `Ignoring unrecognized CSS property: block-progression`.

These warnings did not prevent the build and installation from completing in the tested environment. They have not been established as cursor rendering errors. However, check the final exit status and verify that both output directories contain the expected files; do not treat unrelated build errors as harmless warnings.

The visual behavior of all cursor shapes, hotspots, animations, and both color variants remains under testing. If a cursor is missing, misaligned, or rendered incorrectly, please include the desktop environment/version, the selected variant, and the affected cursor name when reporting it.

## Credits and license

- **Original Future Cursors theme:** [yeyushengfan258/Future-cursors](https://github.com/yeyushengfan258/Future-cursors).
- **Design base:** [Capitaine Cursors](https://github.com/keeferrourke/capitaine-cursors), as credited by the original project.
- **SVG cursor format background:** [KDE: SVG cursors — everything that you need to know about them](https://planet.kde.org/vlad-zahorodnii-2024-10-06-svg-cursors-everything-that-you-need-to-know-about-them/).

The upstream repository identifies the project as **GPL-3.0**. Keep the repository's `LICENSE` file with this fork and consult it for the applicable license terms. This fork's build and installation scripts are additions to the original project; they do not replace the original artwork credits.
