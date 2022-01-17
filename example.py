import asyncio

from aiothinkingcleaner import ThinkingCleaner


async def main(host):
    async with ThinkingCleaner(host, verbose=True) as tc:
        status = await tc.get_status()
        print(status)
        await tc.reboot()
        # await tc.send_command(TCCommand.DOCK)


asyncio.run(main("192.168.3.120"))


# <string name="st_base">On homebase</string>
# <string name="st_base_recon">Reconditioning charging</string>
# <string name="st_base_full">On homebase: Full charging</string>
# <string name="st_base_trickle">Trickle charging</string>
# <string name="st_base_wait">On homebase: Waiting</string>
# <string name="st_plug">Plugged in: Not charging</string>
# <string name="st_plug_recon">Plugged in: Reconditioning charging</string>
# <string name="st_plug_full">Plugged in: Full charging</string>
# <string name="st_plug_trickle">Plugged in: Trickle charging</string>
# <string name="st_plug_wait">Plugged in: Waiting</string>
# <string name="st_stopped">Stopped</string>
# <string name="st_clean">Cleaning</string>
# <string name="st_clean_spot">Spot cleaning</string>
# <string name="st_clean_max">Max cleaning</string>
# <string name="st_dock">Searching homebase</string>
# <string name="st_pickup">Roomba picked up</string>
# <string name="st_remote">Remote control driving</string>
# <string name="st_wait">Waiting for command</string>
# <string name="st_off">Off</string>
# <string name="st_cleanstop">Stopped cleaning</string>
# <string name="error_charge">Charging error</string>
# <string name="error_left_l">Left wheel lifted</string>
# <string name="error_right_l">Right wheel lifted</string>
# <string name="error_cliff">Cliff detected</string>
# <string name="error_left_w">Left wheel problem</string>
# <string name="error_right_w">Right wheel problem</string>
# <string name="error_brush">Main brush stalled</string>
# <string name="error_side">Side brush stalled</string>
# <string name="error">Error</string>
# <string name="st_locate">Find me</string>
# <string name="st_unknown">Unknown</string>
