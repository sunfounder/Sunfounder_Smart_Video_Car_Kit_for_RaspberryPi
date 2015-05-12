/*******************************************************************************#
#           guvcview              http://guvcview.berlios.de                    #
#                                                                               #
#           Paulo Assis <pj.assis@gmail.com>                                    #
#                                                                               #
# This program is free software; you can redistribute it and/or modify          #
# it under the terms of the GNU General Public License as published by          #
# the Free Software Foundation; either version 2 of the License, or             #
# (at your option) any later version.                                           #
#                                                                               #
# This program is distributed in the hope that it will be useful,               #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 #
# GNU General Public License for more details.                                  #
#                                                                               #
# You should have received a copy of the GNU General Public License             #
# along with this program; if not, write to the Free Software                   #
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA     #
#                                                                               #
********************************************************************************/


#include <sys/ioctl.h>
#include <sys/time.h>
#include <getopt.h>
#include <errno.h>
#include <pthread.h>
#include <stdio.h>

#include <linux/videodev2.h>
#include <linux/uvcvideo.h>

#include "../../utils.h"
#include "dynctrl.h"

#ifdef UVCIOC_CTRL_ADD

/* some Logitech webcams have pan/tilt/focus controls */
#define LENGTH_OF_XU_CTR (6)
static struct uvc_xu_control_info xu_ctrls[] = {
    {
        .entity   = UVC_GUID_LOGITECH_MOTOR_CONTROL,
        .selector = XU_MOTORCONTROL_PANTILT_RELATIVE,
        .index    = 0,
        .size     = 4,
        .flags    = UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_MIN | UVC_CONTROL_GET_MAX | UVC_CONTROL_GET_DEF | UVC_CONTROL_AUTO_UPDATE
    },
    {
        .entity   = UVC_GUID_LOGITECH_MOTOR_CONTROL,
        .selector = XU_MOTORCONTROL_PANTILT_RESET,
        .index    = 1,
        .size     = 1,
        .flags    = UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_MIN | UVC_CONTROL_GET_MAX | UVC_CONTROL_GET_RES | UVC_CONTROL_GET_DEF | UVC_CONTROL_AUTO_UPDATE
    },
    {
        .entity   = UVC_GUID_LOGITECH_MOTOR_CONTROL,
        .selector = XU_MOTORCONTROL_FOCUS,
        .index    = 2,
        .size     = 6,
        .flags    = UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_CUR | UVC_CONTROL_GET_MIN | UVC_CONTROL_GET_MAX | UVC_CONTROL_GET_DEF | UVC_CONTROL_AUTO_UPDATE
    },
    {
        .entity   = UVC_GUID_LOGITECH_VIDEO_PIPE,
        .selector = XU_COLOR_PROCESSING_DISABLE,
        .index    = 4,
        .size     = 1,
        .flags    = UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_CUR | UVC_CONTROL_GET_MIN | UVC_CONTROL_GET_MAX | UVC_CONTROL_GET_RES | UVC_CONTROL_GET_DEF | UVC_CONTROL_AUTO_UPDATE
    },
    {
        .entity   = UVC_GUID_LOGITECH_VIDEO_PIPE,
        .selector = XU_RAW_DATA_BITS_PER_PIXEL,
        .index    = 7,
        .size     = 1,
        .flags    = UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_CUR | UVC_CONTROL_GET_MIN | UVC_CONTROL_GET_MAX | UVC_CONTROL_GET_RES | UVC_CONTROL_GET_DEF | UVC_CONTROL_AUTO_UPDATE
    },
    {
        .entity   = UVC_GUID_LOGITECH_USER_HW_CONTROL,
        .selector = XU_HW_CONTROL_LED1,
        .index    = 0,
        .size     = 3,
        .flags    = UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_CUR | UVC_CONTROL_GET_MIN | UVC_CONTROL_GET_MAX | UVC_CONTROL_GET_RES | UVC_CONTROL_GET_DEF | UVC_CONTROL_AUTO_UPDATE
    },

};
#endif

struct uvc_menu_info Logitech_C510_LED_menu[] = {
    {
        .value = 0,
        .name = "Off"
    },

    {
        .value = 1,
        .name = "On",
    },
    {
        .value = 3,
        .name = "Auto",
    },
};

/* some Logitech webcams have pan/tilt/focus controls */
#define LENGTH_OF_XU_MAP (10)

/* mapping for Pan/Tilt/Focus */
struct uvc_xu_control_mapping xu_mappings[] = {
    {
        .id        = V4L2_CID_PAN_RELATIVE,
        .name      = "Pan (relative)",
        .entity    = UVC_GUID_LOGITECH_MOTOR_CONTROL,
        .selector  = XU_MOTORCONTROL_PANTILT_RELATIVE,
        .size      = 16,
        .offset    = 0,
        .v4l2_type = V4L2_CTRL_TYPE_INTEGER,
        .data_type = UVC_CTRL_DATA_TYPE_SIGNED
    },
    {
        .id        = V4L2_CID_TILT_RELATIVE,
        .name      = "Tilt (relative)",
        .entity    = UVC_GUID_LOGITECH_MOTOR_CONTROL,
        .selector  = XU_MOTORCONTROL_PANTILT_RELATIVE,
        .size      = 16,
        .offset    = 16,
        .v4l2_type = V4L2_CTRL_TYPE_INTEGER,
        .data_type = UVC_CTRL_DATA_TYPE_SIGNED
    },
    {
        .id        = V4L2_CID_PAN_RESET,
        .name      = "Pan Reset",
        .entity    = UVC_GUID_LOGITECH_MOTOR_CONTROL,
        .selector  = XU_MOTORCONTROL_PANTILT_RESET,
        .size      = 1,
        .offset    = 0,
        .v4l2_type = V4L2_CTRL_TYPE_BUTTON,
        .data_type = UVC_CTRL_DATA_TYPE_UNSIGNED
    },
    {
        .id        = V4L2_CID_TILT_RESET,
        .name      = "Tilt Reset",
        .entity    = UVC_GUID_LOGITECH_MOTOR_CONTROL,
        .selector  = XU_MOTORCONTROL_PANTILT_RESET,
        .size      = 1,
        .offset    = 1,
        .v4l2_type = V4L2_CTRL_TYPE_BUTTON,
        .data_type = UVC_CTRL_DATA_TYPE_UNSIGNED
    },
    {
        .id        = V4L2_CID_FOCUS,
        .name      = "Focus (absolute)",
        .entity    = UVC_GUID_LOGITECH_MOTOR_CONTROL,
        .selector  = XU_MOTORCONTROL_FOCUS,
        .size      = 8,
        .offset    = 0,
        .v4l2_type = V4L2_CTRL_TYPE_INTEGER,
        .data_type = UVC_CTRL_DATA_TYPE_UNSIGNED
    },
    {
        .id        = V4L2_CID_LED1_MODE,
        .name      = "LED1 Mode",
        .entity    = UVC_GUID_LOGITECH_USER_HW_CONTROL,
        .selector  = XU_HW_CONTROL_LED1,
        .size      = 8,
        .offset    = 0,
        .v4l2_type = V4L2_CTRL_TYPE_INTEGER,
        .data_type = UVC_CTRL_DATA_TYPE_UNSIGNED
    },
    {
        .id        = V4L2_CID_LED1_FREQUENCY,
        .name      = "LED1 Frequency",
        .entity    = UVC_GUID_LOGITECH_USER_HW_CONTROL,
        .selector  = XU_HW_CONTROL_LED1,
        .size      = 8,
        .offset    = 16,
        .v4l2_type = V4L2_CTRL_TYPE_INTEGER,
        .data_type = UVC_CTRL_DATA_TYPE_UNSIGNED
    },
    {
        .id        = V4L2_CID_DISABLE_PROCESSING,
        .name      = "Disable video processing",
        .entity    = UVC_GUID_LOGITECH_VIDEO_PIPE,
        .selector  = XU_COLOR_PROCESSING_DISABLE,
        .size      = 8,
        .offset    = 0,
        .v4l2_type = V4L2_CTRL_TYPE_BOOLEAN,
        .data_type = UVC_CTRL_DATA_TYPE_BOOLEAN
    },
    {
        .id        = V4L2_CID_RAW_BITS_PER_PIXEL,
        .name      = "Raw bits per pixel",
        .entity    = UVC_GUID_LOGITECH_VIDEO_PIPE,
        .selector  = XU_RAW_DATA_BITS_PER_PIXEL,
        .size      = 8,
        .offset    = 0,
        .v4l2_type = V4L2_CTRL_TYPE_INTEGER,
        .data_type = UVC_CTRL_DATA_TYPE_UNSIGNED
    },
    {
        .id        = V4L2_CID_LED1_MODE,
        .name      = "LED1 Mode",
        .entity    = UVC_GUID_LOGITECH_USER_HW_CONTROL_C510,
        .selector  = XU_HW_CONTROL_LED1_C510,
        .size      = 2,
        .offset    = 8,
        .v4l2_type = V4L2_CTRL_TYPE_MENU,
        .data_type = UVC_CTRL_DATA_TYPE_UNSIGNED,
        .menu_count = 3,
        .menu_info = Logitech_C510_LED_menu
    },
};

int initDynCtrls(int fd)
{
    int i = 0;
    int err = 0;

    /*
     * Whaaa use of the obsolote UVCIOC_CTRL_ADD makes the UVCIOC_CTRL_MAP unsuccessful
     */
#ifdef UVCIOC_CTRL_ADD
    /* try to add all controls listed above */
    for(i = 0; i < LENGTH_OF_XU_CTR; i++) {
        fprintf(stderr, "Adding control for %s\n", xu_mappings[i].name);
        if((err = xioctl(fd, UVCIOC_CTRL_ADD, &xu_ctrls[i])) < 0) {
            if(errno != EEXIST)
                DBG("UVCIOC_CTRL_ADD - Error");
            else
                DBG("Control exists");
        }
    }
#endif

    /* after adding the controls, add the mapping now */
    for(i = 0; i < LENGTH_OF_XU_MAP; i++) {
        if((err = xioctl(fd, UVCIOC_CTRL_MAP, &xu_mappings[i])) < 0) {
#ifdef DEBUG
            if(errno == EEXIST) {
                DBG("Mapping exists\n");
            } else if (errno != 0) {
                DBG("UVCIOC_CTRL_MAP - Error at %s: %s (%d)\n", xu_mappings[i].name, strerror(errno), errno);
            }
        } else {
            fprintf(stderr,
                "uvc_xu_control_mapping = {\n"
                "	id        = 0x%08x,\n"
                "	name      = '%s',\n"
                "	selector  = %u,\n"
                "	size      = %u,\n"
                "	offset    = %u,\n"
                "	v4l2_type = %u,\n"
                "	data_type = %u\n"
                "}\n",
                xu_mappings[i].id,
                xu_mappings[i].name,
                xu_mappings[i].selector,
                xu_mappings[i].size,
                xu_mappings[i].offset,
                xu_mappings[i].v4l2_type,
                xu_mappings[i].data_type
            );
        }
#else
        }
#endif
    }
    return 0;
}
