import mcpi.minecraft as minecraft
mc = minecraft.Minecraft.create()
mc.postToChat("This is being done using Raspberry Pi!!!")
mc.player.setPos(0, 100, 0)
