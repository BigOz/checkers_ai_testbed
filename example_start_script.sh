python3 game_runner.py \
    --red_sim_time=$time_for_run \
    --red_max_sim=$sim_for_run \
    --red_max_turns=150 \
    --red_percent_wrong=0 \
    --white_sim_time=1 \
    --white_max_sim=100000 \
    --white_max_turns=150 \
    --white_percent_wrong=0 \
    --filename="example_file.txt" \
    --num_games=10 \
    --num_rounds=150 \
    human_agent \
    monte_carlo_agent

    # agent options include human_agent, monte_carlo_agent, random_agent, and
    # alpha_beta_agent
    # The agent listed first will be the red player, second will be the white
    # player.
    # Parameters can be specified for any agents, but only certain parameters
    # will have any effect on gameply.
    # For alpha_beta_agent and monte_carlo_agent, sim_time specifies how long
    # an agent is allowed to think before having to choose a move
    # For monte_carlo_agent, max_sim specifies how many simulations an agent is
    # allowed to reproduce before haveing to choose a move
    # For alpha_beta_agent, max_turns specifies how many levels deep an agent is
    # allowed to look before choosing a move.
    # For monte_carlo_agent, percent wrong represents how many times in 100 an
    # agent will make a random move rather than an intelligent move.
    # random_agent and human_agent are unaffected by input parameters
    # filename specifies where the results should be written
    # num_games specifies how many games to run
    # num_rounds specifes how many turns to run the game before calling the
    # game a draw
    # -v can be passed to show the board between moves, as well as show insight
    # into strategies from different players.