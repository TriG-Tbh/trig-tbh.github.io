from mcpi.minecraft import Minecraft
from mcpi import block
import time
mc=Minecraft.create()
pos=mc.player.getTilePos()
if pos.z <-40:
    mc.postToChat("Teleportation to safer distance in progress!")
    mc.player.setPos(pos.x,pos.y,-40)
    pos=mc.player.getTilePos()
zpos=pos.z-40
mc.setBlocks(pos.x-1,pos.y+3,pos.z,pos.x+1,pos.y-7,pos.z-88,block.AIR.id)
mc.setBlocks(pos.x,pos.y-1,pos.z,pos.x,
pos.y-7,pos.z,block.BEDROCK_INVISIBLE.id)
mc.setBlocks(pos.x-1,pos.y-1,pos.z,pos.x,
pos.y-7,pos.z,block.BEDROCK_INVISIBLE.id)
mc.setBlocks(pos.x+1,pos.y-1,pos.z,pos.x,
pos.y-7,pos.z,block.BEDROCK_INVISIBLE.id)
mc.setBlocks(pos.x,pos.y-1,pos.z-88,pos.x-1,pos.y-7,pos.z-88,block.BEDROCK_INVISIBLE.id)
mc.setBlocks(pos.x-1,pos.y-1,
pos.z-88,pos.x,pos.y-7,pos.z-88,
block.BEDROCK_INVISIBLE.id)
mc.setBlocks(pos.x+1,
pos.y-1,pos.z-88,pos.x,
pos.y-7,pos.z-88,block.BEDROCK_INVISIBLE.id)
mc.setBlocks(pos.x,pos.y,pos.z,pos.x,
pos.y-7,pos.z-92,block.BEDROCK_INVISIBLE.id)             
mc.setBlocks(pos.x,pos.y,pos.z,pos.x,pos.y,
pos.z-88,block.TNT.id)
mc.setBlock(pos.x,pos.y-1,pos.z,0)
mc.setBlock(pos.x,pos.y-1,pos.z,20)
mc.setBlocks(pos.x-2,pos.y,pos.z-93,
pos.x+2,pos.y,pos.z-97,block.GLOWING_OBSIDIAN.id)
mc.setBlocks(pos.x-1,pos.y+1,pos.z-94,pos.x+1,
pos.y+1,pos.z-96,block.NETHER_REACTOR_CORE.id,1)
mc.setBlock(pos.x,pos.y+2,pos.z-95,
block.REDSTONE_ORE.id)
mc.setBlocks(pos.x-2,pos.y,pos.z-93,
pos.x+2,pos.y,pos.z-97,block.GLOWING_OBSIDIAN.id)
mc.setBlocks(pos.x-1,pos.y+1,pos.z-94,pos.x+1,
pos.y+1,pos.z-96,block.NETHER_REACTOR_CORE.id,1)
mc.setBlock(pos.x,pos.y+2,pos.z-95,
block.REDSTONE_ORE.id)
mc.setBlock(pos.x+1,pos.y+1,pos.z-44,
block.NETHER_REACTOR_CORE.id,2)
mc.setBlock(pos.x-1,pos.y+1,pos.z-44,
block.NETHER_REACTOR_CORE.id,2)
teleport=1
while teleport == 1:
    pos=mc.player.getTilePos()
    if pos.z==zpos:
        mc.player.setPos(pos.x,pos.y,pos.z-24)
        teleport=0
mc.setBlocks(pos.x-1,pos.y,pos.z,pos.x-1,pos.y+1,pos.z,block.OBSIDIAN.id)
