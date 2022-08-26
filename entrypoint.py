from pathlib import Path
import sys
import subprocess

path = Path(sys.argv[1])
compressors = sys.argv[2].split(",")
minRatio = float(sys.argv[3])

dircontent = [p for p in path.rglob('*') if '.git' not in str(p.resolve())]
for p in dircontent:
	print(p)
	if p.is_file() and p.suffix != '.br' and p.suffix != '.gz':
		if "brotli" in compressors:
			subprocess.call(["brotli", "-k", "-f", str(p.resolve())])
			if p.stat().st_size / (p.parent / (p.name + '.br')).stat().st_size < minRatio:
				(p.parent / (p.name + '.br')).unlink()
		if "gzip" in compressors:
			subprocess.call(["gzip", "-12", "-k", "-f", "-n", str(p.resolve())])
			if p.stat().st_size / (p.parent / (p.name + '.gz')).stat().st_size < minRatio:
				(p.parent / (p.name + '.gz')).unlink()
