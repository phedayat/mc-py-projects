from sys import exit

from src.run import Run
from src.config import Config
from src.mpu_wrapper import MpuWrapper
from src.led_and_button import LedWrapper, ButtonWrapper

if __name__=="__main__":
    try:
        # Configure and prepare the MPU
        mpu = MpuWrapper()

        # Configure the LED and off button
        led = LedWrapper()
        off_button = ButtonWrapper()

        # Configure and prepare the run
        config = Config()

        '''
        If we wanted to alter the config from our
        `main` block, we could do this:

            config["new_key1"] = "new_value1"
            config["new_key2"] = "new_value2"
            config["new_key3"] = "new_value3"
            config.save()
        
        Thus the config that'll be used for the run
        will contain the original config options and
        the new ones that were defined here
        '''

        '''
        [NOTE] 
        Below is the template for a 
        *single* run; we should run batch jobs from
        the `main` block.
        
        We could create a BatchRun class to handle this.
        From the `main` block we check whether the `run_id`
        config option is a list or not (alt. we could *always* 
        use a list and check its length). If it isn't, then run
        a single job; otherwise, run a batch job over all
        the run IDs

        [TODO] 
        Figure out how to manage the config per run in
        a batch job
        '''

        run = Run(
            sd_prefix="/sd",
            config=config, 
            mpu=mpu,
            led=led,
            off=off_button,
        )
        run.init()

        # Begin the run
        run.run()
    except KeyboardInterrupt:
        print("SIGINT")
    finally:
        led.blink(5)
        exit(0)
