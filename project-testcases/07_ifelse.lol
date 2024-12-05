HAI
	WAZZUP
		I HAS A choice
		I HAS A input

		I HAS A op1
		I HAS A op2
	BUHBYE

	BTW if w/o MEBBE, 1 only, everything else is invalid
	VISIBLE "1. Compute age"
	VISIBLE "2. Compute tip"
	VISIBLE "3. Compute square area"
	VISIBLE "3. Arithmetic"
	VISIBLE "0. Exit"

	VISIBLE "Choice: "
	GIMMEH choice

	BOTH SAEM choice AN 1
	VISIBLE IT
	O RLY?
		YA RLY
			VISIBLE "Enter birth year: "
			GIMMEH input
			VISIBLE DIFF OF 2022 AN input

	BTW uncomment this portion if you have MEBBE
	BTW else, this portion should be ignored

		MEBBE BOTH SAEM choice AN 2
			VISIBLE "Enter bill cost: "
			GIMMEH input
			VISIBLE "Tip: " + PRODUKT OF input AN 0.1
		MEBBE BOTH SAEM choice AN 3
			VISIBLE "Enter width: "
			GIMMEH input
			VISIBLE "Square Area: " + PRODUKT OF input AN input
		MEBBE BOTH SAEM choice AN 4
			VISIBLE "Enter op1: "
			GIMMEH op1

			VISIBLE "Enter op2: "
			GIMMEH op2

			VISIBLE "Operation"
			VISIBLE "[1] Multiply"
			VISIBLE "[2] Division"
			VISIBLE "[3] Addition"
			VISIBLE "[4] Modulo"
			GIMMEH choice

			BOTH SAEM choice AN 1
			O RLY?
				YA RLY
					VISIBLE "Result: " + SUM OF op1 AN op2
				MEBBE BOTH SAEM choice AN 2
					VISIBLE "Result: " + SUM OF op1 AN op2
				MEBBE BOTH SAEM choice AN 3
					VISIBLE "Result: " + SUM OF op1 AN op2
				MEBBE BOTH SAEM choice AN 4
					VISIBLE "Result: " + SUM OF op1 AN op2
				NO WAI 
					VISIBLE "Operation not found"
			OIC
		MEBBE BOTH SAEM choice AN 0
			VISIBLE "Goodbye"

		NO WAI
			VISIBLE "Invalid Input!"
	OIC

	DIFFRINT BIGGR OF 3 AN choice AN 3
	O RLY?
		YA RLY
			VISIBLE "Invalid input is > 3."
	OIC

KTHXBYE