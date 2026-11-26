import sys
import rasterio
import pyogrio

packages = ['numpy', 'scipy', 'pandas', 'shapely', 'pyogrio', 'geopandas', 'rasterio', 'matplotlib']
pkg_versions = {}
for pkg in packages:
    mod = __import__(pkg)
    pkg_versions[pkg] = getattr(mod, '__version__', 'unknown')

with rasterio.open('seoul_s2_20260516.tif') as src:
    count = src.count
    width = src.width
    height = src.height
    res_x, res_y = src.res
    crs = str(src.crs)

layers = pyogrio.list_layers('seoul_boundary.gpkg')
layer_counts = {}
for l in layers[:, 0]:
    info = pyogrio.read_info('seoul_boundary.gpkg', layer=l)
    layer_counts[l] = info['features']

lines = []
lines.append('=== 환경 검증 결과 ===')
lines.append(f'Python 버전: {sys.version.split()[0]}')
lines.append('설치 방법: uv (uv venv --python 3.12 .venv, uv pip install)')
lines.append('\n[패키지 버전]')
for k, v in pkg_versions.items():
    lines.append(f'  {k}: {v}')

lines.append('\n[영상 확인: seoul_s2_20260516.tif]')
lines.append(f'  밴드 수: {count}')
lines.append(f'  화소 수: {width} × {height} (가로 × 세로)')
lines.append(f'  화소 크기: {res_x} m × {res_y} m')
lines.append(f'  좌표계: {crs}')

lines.append('\n[경계 데이터 확인: seoul_boundary.gpkg]')
for l, c in layer_counts.items():
    lines.append(f'  레이어 {l}: {c}개 피처')

lines.append(f'\n기준값 대조 요약:')
lines.append(f'  밴드 {count}개 · {width} × {height} 화소 · {int(res_x)} m · {crs} · seoul {layer_counts.get("seoul", 0)}개 · gu {layer_counts.get("gu", 0)}개')

content = '\n'.join(lines)
print(content)

with open('env_check.txt', 'w', encoding='utf-8') as f:
    f.write(content + '\n')
