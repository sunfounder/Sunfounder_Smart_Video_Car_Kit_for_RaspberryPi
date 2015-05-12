/*******************************************************************************
#                                                                              #
#      MJPG-streamer allows to stream JPG frames from an input-plugin          #
#      to several output plugins                                               #
#                                                                              #
#      Copyright (C) 2007 Tom Stöveken                                         #
#                                                                              #
# This program is free software; you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation; version 2 of the License.                      #
#                                                                              #
# This program is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU General Public License for more details.                                 #
#                                                                              #
# You should have received a copy of the GNU General Public License            #
# along with this program; if not, write to the Free Software                  #
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA    #
#                                                                              #
*******************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/ioctl.h>
#include <errno.h>
#include <signal.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <getopt.h>
#include <pthread.h>
#include <syslog.h>

#include <linux/types.h>          /* for videodev2.h */
#include <linux/videodev2.h>

#include "../../mjpg_streamer.h"
#include "../../utils.h"

#include "testpictures.h"

#define INPUT_PLUGIN_NAME "TESTPICTURE input plugin"

/* private functions and variables to this plugin */
static pthread_t   worker;
static globals     *pglobal;
static pthread_mutex_t controls_mutex;
static int plugin_number;

void *worker_thread(void *);
void worker_cleanup(void *);
void help(void);

static int delay = 1000;

/* details of converted JPG pictures */
struct pic {
    const unsigned char *data;
    const int size;
};

/* lookup pictures by resolution */
#define ENTRY(res, pic1, pic2) { res, { { pic1, sizeof(pic1) }, { pic2, sizeof(pic2) } } }
static struct pictures {
    const char *resolution;
    struct pic sequence[2];
} picture_lookup[] = {
    ENTRY("960x720", PIC_960x720_1, PIC_960x720_2),
    ENTRY("640x480", PIC_640x480_1, PIC_640x480_2),
    ENTRY("320x240", PIC_320x240_1, PIC_320x240_2),
    ENTRY("160x120", PIC_160x120_1, PIC_160x120_2)
};

struct pictures *pics;

/*** plugin interface functions ***/

/******************************************************************************
Description.: parse input parameters
Input Value.: param contains the command line string and a pointer to globals
Return Value: 0 if everything is ok
******************************************************************************/
int input_init(input_parameter *param, int id)
{
    int i;

    pics = &picture_lookup[1];

    if(pthread_mutex_init(&controls_mutex, NULL) != 0) {
        IPRINT("could not initialize mutex variable\n");
        exit(EXIT_FAILURE);
    }

    param->argv[0] = INPUT_PLUGIN_NAME;
    param->global->in[id].name = malloc((strlen(INPUT_PLUGIN_NAME) + 1) * sizeof(char));
    sprintf(param->global->in[id].name, INPUT_PLUGIN_NAME);

    /* show all parameters for DBG purposes */
    for(i = 0; i < param->argc; i++) {
        DBG("argv[%d]=%s\n", i, param->argv[i]);
    }

    reset_getopt();
    while(1) {
        int option_index = 0, c = 0;
        static struct option long_options[] = {
            {"h", no_argument, 0, 0
            },
            {"help", no_argument, 0, 0},
            {"d", required_argument, 0, 0},
            {"delay", required_argument, 0, 0},
            {"r", required_argument, 0, 0},
            {"resolution", required_argument, 0, 0},
            {0, 0, 0, 0}
        };

        c = getopt_long_only(param->argc, param->argv, "", long_options, &option_index);

        /* no more options to parse */
        if(c == -1) break;

        /* unrecognized option */
        if(c == '?') {
            help();
            return 1;
        }

        switch(option_index) {
            /* h, help */
        case 0:
        case 1:
            DBG("case 0,1\n");
            help();
            return 1;
            break;

            /* d, delay */
        case 2:
        case 3:
            DBG("case 2,3\n");
            delay = atoi(optarg);
            break;

            /* r, resolution */
        case 4:
        case 5:
            DBG("case 4,5\n");
            for(i = 0; i < LENGTH_OF(picture_lookup); i++) {
                if(strcmp(picture_lookup[i].resolution, optarg) == 0) {
                    pics = &picture_lookup[i];
                    break;
                }
            }
            break;

        default:
            DBG("default case\n");
            help();
            return 1;
        }
    }

    pglobal = param->global;

    IPRINT("delay.............: %i\n", delay);
    IPRINT("resolution........: %s\n", pics->resolution);

    // add some dummy controls
    pglobal->in[id].parametercount = 3;
    pglobal->in[id].in_parameters = (control*)calloc(3, sizeof(control));

    /*
     *struct v4l2_queryctrl ctrl;
    int value;
    struct v4l2_querymenu *menuitems;
        In the case the control a V4L2 ctrl this variable will specify
        that the control is a V4L2_CTRL_CLASS_USER control or not.
        For non V4L2 control it is not acceptable, leave it 0.

    int class_id;
    int group;*/
    /*
       Used in the VIDIOC_QUERYCTRL ioctl for querying controls *
            struct v4l2_queryctrl {
                __u32		     id;
                __u32		     type;
                __u8		     name[32];
                __s32		     minimum;
                __s32		     maximum;
                __s32		     step;
                __s32		     default_value;
                __u32                flags;
                __u32		     reserved[2];
            };
     */
    pglobal->in[id].in_parameters[0].ctrl.id = 120;
    pglobal->in[id].in_parameters[0].ctrl.type = V4L2_CTRL_TYPE_INTEGER;
    sprintf((char*)pglobal->in[id].in_parameters[0].ctrl.name, "Foo integer control");
    pglobal->in[id].in_parameters[0].value = 100;
    pglobal->in[id].in_parameters[0].ctrl.minimum = 0;
    pglobal->in[id].in_parameters[0].ctrl.maximum = 512;
    pglobal->in[id].in_parameters[0].ctrl.step = 1;
    pglobal->in[id].in_parameters[0].ctrl.default_value = 12;

    // add pan and tilt
    pglobal->in[id].in_parameters[1].ctrl.id = V4L2_CID_PAN_RELATIVE;
    pglobal->in[id].in_parameters[1].ctrl.type = V4L2_CTRL_TYPE_INTEGER;
    sprintf((char*)pglobal->in[id].in_parameters[1].ctrl.name, "Pan test Ctrl");
    pglobal->in[id].in_parameters[1].value = 0;
    pglobal->in[id].in_parameters[1].group = 1;
    pglobal->in[id].in_parameters[1].ctrl.minimum = 0;
    pglobal->in[id].in_parameters[1].ctrl.maximum = 1024;
    pglobal->in[id].in_parameters[1].ctrl.step = 1;
    pglobal->in[id].in_parameters[1].ctrl.default_value = 0;

    pglobal->in[id].in_parameters[2].ctrl.id = V4L2_CID_TILT_RELATIVE;
    pglobal->in[id].in_parameters[2].ctrl.type = V4L2_CTRL_TYPE_INTEGER;
    sprintf((char*)pglobal->in[id].in_parameters[2].ctrl.name, "Tilt test Ctrl");
    pglobal->in[id].in_parameters[2].value = 0;
    pglobal->in[id].in_parameters[2].group = 1;
    pglobal->in[id].in_parameters[2].ctrl.minimum = 0;
    pglobal->in[id].in_parameters[2].ctrl.maximum = 1024;
    pglobal->in[id].in_parameters[2].ctrl.step = 1;
    pglobal->in[id].in_parameters[2].ctrl.default_value = 0;
    return 0;
}

/******************************************************************************
Description.: stops the execution of the worker thread
Input Value.: -
Return Value: 0
******************************************************************************/
int input_stop(int id)
{
    DBG("will cancel input thread\n");
    pthread_cancel(worker);

    return 0;
}

/******************************************************************************
Description.: starts the worker thread and allocates memory
Input Value.: -
Return Value: 0
******************************************************************************/
int input_run(int id)
{
    pglobal->in[id].buf = malloc(256 * 1024);
    if(pglobal->in[id].buf == NULL) {
        fprintf(stderr, "could not allocate memory\n");
        exit(EXIT_FAILURE);
    }

    if(pthread_create(&worker, 0, worker_thread, NULL) != 0) {
        free(pglobal->in[id].buf);
        fprintf(stderr, "could not start worker thread\n");
        exit(EXIT_FAILURE);
    }
    pthread_detach(worker);

    return 0;
}

/******************************************************************************
Description.: print help message
Input Value.: -
Return Value: -
******************************************************************************/
void help(void)
{
    fprintf(stderr, " ---------------------------------------------------------------\n" \
    " Help for input plugin..: "INPUT_PLUGIN_NAME"\n" \
    " ---------------------------------------------------------------\n" \
    " The following parameters can be passed to this plugin:\n\n" \
    " [-d | --delay ]........: delay to pause between frames\n" \
    " [-r | --resolution]....: can be 960x720, 640x480, 320x240, 160x120\n"
    " ---------------------------------------------------------------\n");
}

/******************************************************************************
Description.: copy a picture from testpictures.h and signal this to all output
              plugins, afterwards switch to the next frame of the animation.
Input Value.: arg is not used
Return Value: NULL
******************************************************************************/
void *worker_thread(void *arg)
{
    int i = 0;

    /* set cleanup handler to cleanup allocated ressources */
    pthread_cleanup_push(worker_cleanup, NULL);

    while(!pglobal->stop) {

        /* copy JPG picture to global buffer */
        pthread_mutex_lock(&pglobal->in[plugin_number].db);

        i = (i + 1) % LENGTH_OF(pics->sequence);
        pglobal->in[plugin_number].size = pics->sequence[i].size;
        memcpy(pglobal->in[plugin_number].buf, pics->sequence[i].data, pglobal->in[plugin_number].size);

        /* signal fresh_frame */
        pthread_cond_broadcast(&pglobal->in[plugin_number].db_update);
        pthread_mutex_unlock(&pglobal->in[plugin_number].db);

        usleep(1000 * delay);
    }

    IPRINT("leaving input thread, calling cleanup function now\n");
    pthread_cleanup_pop(1);

    return NULL;
}

/******************************************************************************
Description.: this functions cleans up allocated ressources
Input Value.: arg is unused
Return Value: -
******************************************************************************/
void worker_cleanup(void *arg)
{
    static unsigned char first_run = 1;

    if(!first_run) {
        DBG("already cleaned up ressources\n");
        return;
    }

    first_run = 0;
    DBG("cleaning up ressources allocated by input thread\n");

    if(pglobal->in[plugin_number].buf != NULL) free(pglobal->in[plugin_number].buf);
}

/******************************************************************************
Description.: process commands, allows to set v4l2 controls
Input Value.: * control specifies the selected v4l2 control's id
                see struct v4l2_queryctr in the videodev2.h
              * value is used for control that make use of a parameter.
Return Value: depends in the command, for most cases 0 means no errors and
              -1 signals an error. This is just rule of thumb, not more!
******************************************************************************/
int input_cmd(int plugin_number, unsigned int control_id, unsigned int group, int value, char *value_string)
{
    if (control_id < 3)
        pglobal->in[plugin_number].in_parameters[control_id].value = value;
    return 0;
}


