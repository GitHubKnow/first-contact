from armoriq_sdk import ArmorIQClient


class RuleBasedAgent:

    def __init__(self):
        self.client = ArmorIQClient()


    # -------------------------
    # Rule based planner
    # -------------------------

    def create_plan(self, prompt):

        if prompt == "show_sales":

            return {
                "steps": [
                    {
                        "mcp": "sales-mcp",
                        "action": "fetch_sales",
                        "params": {}
                    }
                ]
            }


        elif prompt == "analyze_sales":

            return {
                "steps": [
                    {
                        "mcp": "sales-mcp",
                        "action": "analyze_sales",
                        "params": {}
                    }
                ]
            }


        else:
            raise Exception("Unknown command")


    # -------------------------
    # Execute through ArmorIQ
    # -------------------------

    def execute(self, prompt):

        plan = self.create_plan(prompt)


        print("\nPLAN:")
        print(plan)


        # Capture execution plan
        plan_capture = self.client.capture_plan(
            llm="rule-based-planner",
            prompt=prompt,
            plan=plan
        )


        print("\nPLAN CAPTURE:")
        print(plan_capture)



        # Generate intent token
        intent_token = self.client.get_intent_token(
            plan_capture
        )


        print("\nINTENT TOKEN GENERATED")



        # Get first step
        step = plan["steps"][0]


        # Execute through ArmorIQ MCP proxy
        result = self.client.invoke(
            mcp=step["mcp"],
            action=step["action"],
            intent_token=intent_token,
            params=step["params"]
        )


        return result
