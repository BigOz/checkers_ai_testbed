echo 'compiling with cython...';
cython -3 gamePlay.py -o gamePlay.c;
cython -3 getAllPossibleMoves.py -o getAllPossibleMoves.c;
cython -3 agents/monte_carlo_agent.py -o agents/monte_carlo_agent.c;
cython -3 agents/alpha_beta_agent.py -o agents/alpha_beta_agent.c;

echo 'removing old .so files...';
rm *.so agents/*.so;

echo 'compiling .c files with gcc...'
gcc -shared -I/usr/include/python3.5m -fPIC -pthread -fwrapv -O3 -Wall -fno-strict-aliasing gamePlay.c -o gamePlay.so;
gcc -shared -I/usr/include/python3.5m -fPIC -pthread -fwrapv -O3 -Wall -fno-strict-aliasing getAllPossibleMoves.c -o getAllPossibleMoves.so;
gcc -shared -I/usr/include/python3.5m -fPIC -pthread -fwrapv -O3 -Wall -fno-strict-aliasing agents/monte_carlo_agent.c -o agents/monte_carlo_agent.so;
gcc -shared -I/usr/include/python3.5m -fPIC -pthread -fwrapv -O3 -Wall -fno-strict-aliasing agents/alpha_beta_agent.c -o agents/alpha_beta_agent.so;

echo 'removing .c files...';
rm *.c agents/*.c;

echo 'done.';