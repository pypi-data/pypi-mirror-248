from systems.provided.futures_chapter15.basesystem import futures_system
system=futures_system()
system.accounts.portfolio().stats() ## see some statistics
system.accounts.portfolio().curve().plot() ## plot an account curve
system.accounts.portfolio().percent.curve().plot() ## plot an account curve in percentage terms
system.accounts.pandl_for_instrument("US10").percent.stats() ## produce % statistics for a 10 year bond
system.accounts.pandl_for_instrument_forecast("EDOLLAR", "carry").sharpe() ## Sharpe for a specific trading rule variation
