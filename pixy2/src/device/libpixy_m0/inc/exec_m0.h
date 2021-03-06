//
// begin license header
//
// This file is part of Pixy CMUcam5 or "Pixy" for short
//
// All Pixy source code is provided under the terms of the
// GNU General Public License v2 (http://www.gnu.org/licenses/gpl-2.0.html).
// Those wishing to use Pixy source code, software and/or
// technologies under different licensing terms should contact us at
// cmucam@cs.cmu.edu. Such licensing terms are available for
// all portions of the Pixy codebase presented here.
//
// end license header
//

#ifndef _EXEC_M0_H
#define _EXEC_M0_H

void setTimer(uint32_t *timer);
uint32_t getTimer(uint32_t timer);
void delayus(uint32_t us);

int exec_init(void);
uint32_t exec_running(void);
int32_t exec_stop(void);
int32_t exec_run(uint8_t *prog);
void exec_loop(void);

#endif
