# Shared paths for the Money Mirage v3 tools. Run every tool FROM the episode folder (money-mirage/episodes/epNN).
import os, sys, json
MM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # money-mirage/mm3
REPO = os.path.dirname(os.path.dirname(MM))                                # media-engine
HERE = os.getcwd()                                                          # the episode folder
ENG = os.path.join(MM, 'engine'); LIB = os.path.join(MM, 'library')
EPC = json.load(open(os.path.join(HERE, 'episode.json')))
SRC = os.path.join(REPO, EPC.get('src', os.path.relpath(os.path.join(HERE, 'src'), REPO)))
DEP = os.path.join(REPO, 'outputs/depth'); DEPTH_JOBS = EPC.get('depth_jobs', [])
SFX = os.path.join(LIB, 'sfx') + '/'; MUSIC = os.path.join(LIB, 'music')
sys.path.insert(0, os.path.join(REPO, 'bhugol-v2/motion')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True
