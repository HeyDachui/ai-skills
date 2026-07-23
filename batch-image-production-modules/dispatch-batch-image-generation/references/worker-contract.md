# Worker contract

A worker packet is bounded work, not permission to claim more jobs.

The worker:

1. uses only listed job IDs;
2. reads only listed references;
3. sends the exact listed prompt;
4. writes the target and receipt locally;
5. records network and moderation outcomes;
6. stops after the packet;
7. returns paths and short status, not embedded image data.

The controller reconciles completion from local evidence.
