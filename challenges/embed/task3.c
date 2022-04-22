#include <stdio.h>
#include <stdint.h>

/* Task3 Description
 * -----------------
 *
 * This file contains some sample Queue APIs for a pre-emptive, priority based scheduling RTOS.
 * You need to write parts of a multitasking application for this RTOS. Focus will be on two
 * tasks of interest, TaskA and TaskB. TaskA sends a message of the format <ID, char array>
 * to a Queue. TaskB is responsible for retrieving messages from the same Queue.
 * TaskA sends messages asynchronously without waiting. While TaskB waits for 10 ticks in
 * case no message is available.

 * In addition to filling TaskA and TaskB functions, please identify any synchronization issues
 * faced by the application. You can put your thoughts as comments in the task functions.
 * Also propose a fault tolerant design for this application. Please state your assumptions
 * (if any) about the RTOS internals.
 *
 */
typedef struct RTOS_QUEUE RTOS_QUEUE;

RTOS_QUEUE *RTOS_Create_Queue(size_t numElems, size_t perElemSize);
int RTOS_SendTo_Queue(RTOS_QUEUE *txQueue, void *txBuffer, unsigned waitDurationTicks);
int RTOS_RecvFrom_Queue(RTOS_QUEUE *rxQueue, void *rxBuffer, unsigned waitDurationTicks);

RTOS_QUEUE *q;

struct QMessage
{
    uint8_t qID;
    char qData[20];
} qMessage;

// TaskA function to be completed
void TaskA(void *Params)
{

}

// TaskB function to be completed
void TaskB(void *Params)
{

}

