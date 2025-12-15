from django.core.management.base import BaseCommand
from lessons.models import LearningPath, Lesson, Quiz, Question, Answer


class Command(BaseCommand):
    help = "Populate lessons with business scenario-based content"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating learning paths and scenario lessons...")

        # Create main learning path
        path, created = LearningPath.objects.get_or_create(
            title="Business Simulation Adventures",
            defaults={
                "description": "Learn financial literacy through interactive business simulations. From lemonade stands to online stores, build real business skills!",
                "icon": "💼",
                "difficulty": "intermediate",
                "min_age": 8,
                "max_age": 15,
                "total_duration": 780,
                "certificate_available": True,
                "order": 1,
                "is_active": True,
            },
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created: {path.title}"))

        # Scenario-based lessons
        lessons_data = [
            {
                "title": "Summer Lemonade Stand",
                "description": "Learn basic costs, pricing strategy, and profit calculation by running a virtual lemonade stand.",
                "icon": "🍋",
                "duration": 60,
                "order": 1,
                "learning_objectives": [
                    "Calculate basic costs (fixed + variable)",
                    "Understand pricing strategy and price elasticity",
                    "Experience supply and demand dynamics",
                    "Learn profit = revenue - costs formula",
                    "Recognize marketing's impact on sales",
                ],
                "quiz_questions": [
                    {
                        "question": "You buy lemons for $0.50 each and sugar for $5. If you make 20 cups of lemonade, what are your total costs?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "$15 (10 lemons × $0.50 + $5 sugar)",
                                "correct": True,
                            },
                            {"text": "$10 (just the lemons)", "correct": False},
                            {"text": "$5 (just the sugar)", "correct": False},
                            {"text": "$20", "correct": False},
                        ],
                        "explanation": "Total costs = variable costs (lemons) + fixed costs (sugar). You need 10 lemons for 20 cups at $0.50 each = $5, plus $5 for sugar = $15 total.",
                    },
                    {
                        "question": "If you sell lemonade at $2 per cup and sell 15 cups, but your costs were $15, what is your profit?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "$15 profit ($30 revenue - $15 costs)",
                                "correct": True,
                            },
                            {"text": "$30 profit", "correct": False},
                            {"text": "$0 profit (break even)", "correct": False},
                            {"text": "$45 profit", "correct": False},
                        ],
                        "explanation": "Profit = Revenue - Costs. Revenue = 15 cups × $2 = $30. Costs = $15. Profit = $30 - $15 = $15.",
                    },
                    {
                        "question": "What is price elasticity?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "How price changes affect customer demand - higher prices mean fewer buyers",
                                "correct": True,
                            },
                            {
                                "text": "How stretchy your lemonade cups are",
                                "correct": False,
                            },
                            {"text": "The cost of making lemonade", "correct": False},
                            {
                                "text": "How fast you can sell lemonade",
                                "correct": False,
                            },
                        ],
                        "explanation": "Price elasticity measures how sensitive customers are to price changes. If you charge too much, demand drops!",
                    },
                    {
                        "question": "You spend $8 on colorful posters to advertise. Why is this an investment?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "It costs money now but should attract more customers and increase sales later",
                                "correct": True,
                            },
                            {
                                "text": "It's not an investment, it's just a waste of money",
                                "correct": False,
                            },
                            {
                                "text": "It makes your stand look pretty",
                                "correct": False,
                            },
                            {"text": "It's required by law", "correct": False},
                        ],
                        "explanation": "Marketing is an investment - you spend money upfront to generate more revenue through increased customer traffic.",
                    },
                ],
            },
            {
                "title": "Toy Shop Tycoon",
                "description": "Manage inventory, understand fixed vs. variable costs, and balance product mix in a retail simulation.",
                "icon": "🧸",
                "duration": 90,
                "order": 2,
                "learning_objectives": [
                    "Understand fixed vs. variable costs",
                    "Learn inventory management and stock balancing",
                    "Experience rent and location decisions",
                    "Understand labor costs and productivity",
                    "Practice pricing strategy with multiple products",
                ],
                "quiz_questions": [
                    {
                        "question": "What is a fixed cost?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "A cost you pay regardless of how much you sell (like rent)",
                                "correct": True,
                            },
                            {
                                "text": "A cost that changes based on sales",
                                "correct": False,
                            },
                            {
                                "text": "A cost that's broken and can't be changed",
                                "correct": False,
                            },
                            {"text": "The cost of toys", "correct": False},
                        ],
                        "explanation": "Fixed costs (rent, insurance) stay the same whether you sell 1 toy or 100 toys. Variable costs change with sales volume.",
                    },
                    {
                        "question": "You rent a shop for $60/month and buy toys for $200. After selling everything for $400, what's your profit?",
                        "type": "multiple",
                        "answers": [
                            {"text": "$140 ($400 - $60 - $200)", "correct": True},
                            {"text": "$200", "correct": False},
                            {"text": "$340", "correct": False},
                            {"text": "$400", "correct": False},
                        ],
                        "explanation": "Profit = Revenue - All Costs. $400 revenue - $60 rent - $200 toys = $140 profit.",
                    },
                    {
                        "question": "Why is unsold inventory a problem?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Money is tied up in products you can't use, and you might not sell them",
                                "correct": True,
                            },
                            {"text": "It takes up space only", "correct": False},
                            {"text": "It's not a problem at all", "correct": False},
                            {
                                "text": "You can always sell it eventually",
                                "correct": False,
                            },
                        ],
                        "explanation": "Unsold inventory means your cash is stuck in products. This money could be used elsewhere, and the products might never sell.",
                    },
                    {
                        "question": "You can hire an assistant for $40 who helps you serve 5 more customers per hour. If each customer spends $10, is it worth it?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Yes, if those 5 extra customers generate more than $40 in profit",
                                "correct": True,
                            },
                            {
                                "text": "No, labor costs always hurt profit",
                                "correct": False,
                            },
                            {"text": "Yes, always hire more people", "correct": False},
                            {"text": "It doesn't matter", "correct": False},
                        ],
                        "explanation": "Labor is worth it when the additional revenue exceeds the cost. 5 customers × $10 = $50 revenue, minus product costs, should exceed $40.",
                    },
                ],
            },
            {
                "title": "Busy Bakery Boss",
                "description": "Master production planning, ingredient costs, freshness management, and time-based pricing in a food business.",
                "icon": "🧁",
                "duration": 75,
                "order": 3,
                "learning_objectives": [
                    "Production planning and timing",
                    "Ingredient cost calculation",
                    "Freshness as value (time decay)",
                    "Product mix optimization",
                    "Pricing based on perceived value",
                ],
                "quiz_questions": [
                    {
                        "question": "Why do day-old baked goods sell for less?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Freshness decreases perceived value - customers won't pay full price for older items",
                                "correct": True,
                            },
                            {"text": "They cost less to make", "correct": False},
                            {
                                "text": "It's illegal to charge full price",
                                "correct": False,
                            },
                            {"text": "Bakers are just being nice", "correct": False},
                        ],
                        "explanation": "Time decay: Fresh food has higher value. As items age, customers perceive less value and expect discounts.",
                    },
                    {
                        "question": "Cupcakes cost $0.75 in ingredients and 30 minutes to bake. If you value your time at $10/hour, what's your minimum price?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "$5.75 or more ($0.75 + $5 for labor)",
                                "correct": True,
                            },
                            {"text": "$0.75", "correct": False},
                            {"text": "$10.75", "correct": False},
                            {"text": "$3.00", "correct": False},
                        ],
                        "explanation": "Cost = materials + labor. $0.75 ingredients + (0.5 hours × $10/hour) = $5.75 minimum before profit margin.",
                    },
                    {
                        "question": "You baked 20 cupcakes but only sold 15. What happened to the wasted 5 cupcakes?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Lost money - you paid for ingredients and time but got no revenue",
                                "correct": True,
                            },
                            {"text": "No impact on profit", "correct": False},
                            {"text": "You can sell them next week", "correct": False},
                            {
                                "text": "The ingredients magically return",
                                "correct": False,
                            },
                        ],
                        "explanation": "Waste = lost money. You spent resources (ingredients + time) but generated zero revenue from unsold items.",
                    },
                    {
                        "question": "What's the advantage of offering multiple products (cupcakes, cookies, bread)?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Different customers want different things - you reach more buyers",
                                "correct": True,
                            },
                            {
                                "text": "It makes your bakery look bigger",
                                "correct": False,
                            },
                            {
                                "text": "You can charge more for everything",
                                "correct": False,
                            },
                            {"text": "It's more fun to bake", "correct": False},
                        ],
                        "explanation": "Product diversification reaches different customer segments and spreads risk - if one product doesn't sell well, others might.",
                    },
                ],
            },
            {
                "title": "Farm Fresh Stand",
                "description": "Learn about time value of money, opportunity cost, crop investment decisions, and seasonal demand patterns.",
                "icon": "🌾",
                "duration": 120,
                "order": 4,
                "learning_objectives": [
                    "Time value of money (growing cycles)",
                    "Opportunity cost (fast vs. slow crops)",
                    "Risk management (weather, pests)",
                    "Seasonal demand fluctuations",
                    "Investment returns over time",
                ],
                "quiz_questions": [
                    {
                        "question": "What is opportunity cost?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "What you give up by choosing one option over another",
                                "correct": True,
                            },
                            {"text": "The cost of buying seeds", "correct": False},
                            {"text": "The price of opportunities", "correct": False},
                            {"text": "A discount opportunity", "correct": False},
                        ],
                        "explanation": "Opportunity cost is the value of the next best alternative you didn't choose. Planting lettuce means giving up what you could have earned from tomatoes.",
                    },
                    {
                        "question": "Lettuce grows in 1 week and earns $25. Pumpkins grow in 6 weeks and earn $60. Which has better weekly return?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Lettuce - $25/week vs. pumpkins $10/week ($60÷6)",
                                "correct": True,
                            },
                            {
                                "text": "Pumpkins - bigger total profit",
                                "correct": False,
                            },
                            {"text": "They're exactly the same", "correct": False},
                            {"text": "Can't compare them", "correct": False},
                        ],
                        "explanation": "Time matters! Lettuce: $25/week. Pumpkins: $60÷6 weeks = $10/week. You could grow 6 lettuce crops while 1 pumpkin grows.",
                    },
                    {
                        "question": "Why would you buy crop insurance?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Protect against losses from weather or pests that could destroy your investment",
                                "correct": True,
                            },
                            {"text": "It's required by law", "correct": False},
                            {"text": "To make more money", "correct": False},
                            {"text": "It makes crops grow faster", "correct": False},
                        ],
                        "explanation": "Insurance transfers risk. You pay a premium to protect against potential large losses from uncontrollable events.",
                    },
                    {
                        "question": "Pumpkins sell for $15 normally but $20 in fall. When should you harvest and sell?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Wait for fall demand - timing matters for maximum profit",
                                "correct": True,
                            },
                            {"text": "Sell immediately at any price", "correct": False},
                            {"text": "Timing doesn't matter", "correct": False},
                            {"text": "Hold them forever", "correct": False},
                        ],
                        "explanation": "Seasonal demand creates price variations. Strategic timing can significantly increase revenue for the same product.",
                    },
                ],
            },
            {
                "title": "Mobile Car Wash",
                "description": "Understand service business pricing, time management, customer retention, and the value of quality service.",
                "icon": "🚗",
                "duration": 80,
                "order": 5,
                "learning_objectives": [
                    "Service pricing vs. product pricing",
                    "Time management and productivity",
                    "Customer service quality impact",
                    "Building repeat customers",
                    "Operating expenses in service businesses",
                ],
                "quiz_questions": [
                    {
                        "question": "What's the main difference between service and product businesses?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Services sell time and labor, products sell physical goods",
                                "correct": True,
                            },
                            {
                                "text": "Services are always more profitable",
                                "correct": False,
                            },
                            {"text": "Products are easier to run", "correct": False},
                            {"text": "There's no difference", "correct": False},
                        ],
                        "explanation": "Service businesses sell labor and expertise. Your time and skill are the product, not a physical item.",
                    },
                    {
                        "question": "A customer gives you a 5-star review. Why is this valuable?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Good reviews attract new customers and build trust - cheaper than advertising",
                                "correct": True,
                            },
                            {"text": "Reviews don't matter", "correct": False},
                            {"text": "You can sell the review", "correct": False},
                            {"text": "It just makes you feel good", "correct": False},
                        ],
                        "explanation": "Reviews are social proof. They reduce customer acquisition costs by building trust and attracting customers through reputation.",
                    },
                    {
                        "question": "Why are repeat customers more valuable than new customers?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "They cost less to acquire and trust you already, leading to more business",
                                "correct": True,
                            },
                            {"text": "They always pay more", "correct": False},
                            {"text": "They're not more valuable", "correct": False},
                            {
                                "text": "New customers are always better",
                                "correct": False,
                            },
                        ],
                        "explanation": "Customer Lifetime Value matters. Repeat customers have zero acquisition cost and higher loyalty - they're more profitable.",
                    },
                    {
                        "question": "You can wash cars quickly (low quality) or slowly (high quality). Which strategy is better long-term?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "High quality - satisfied customers return and refer others",
                                "correct": True,
                            },
                            {
                                "text": "Fast and cheap - quantity over quality",
                                "correct": False,
                            },
                            {"text": "It doesn't matter", "correct": False},
                            {"text": "Always be the fastest", "correct": False},
                        ],
                        "explanation": "Quality builds reputation. While speed generates immediate revenue, quality creates sustainable business through referrals and repeat customers.",
                    },
                ],
            },
            {
                "title": "Pet Sitting Service",
                "description": "Learn time management, reputation building, scheduling constraints, and customer relationship management.",
                "icon": "🐾",
                "duration": 70,
                "order": 6,
                "learning_objectives": [
                    "Service pricing based on time and complexity",
                    "Scheduling and time management",
                    "Building trust and reputation",
                    "Customer relationship management",
                    "Scaling a service business",
                ],
                "quiz_questions": [
                    {
                        "question": "Why should overnight pet sitting cost more than a 30-minute visit?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "More time commitment and responsibility - opportunity cost is higher",
                                "correct": True,
                            },
                            {"text": "Just to be greedy", "correct": False},
                            {"text": "It doesn't need to cost more", "correct": False},
                            {"text": "Nighttime is scary", "correct": False},
                        ],
                        "explanation": "Pricing reflects time, responsibility, and opportunity cost. Overnight sitting prevents you from doing other things - that time has value.",
                    },
                    {
                        "question": "You're fully booked but a new client offers double pay. Should you accept?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "No - overbooking risks poor service quality and damages your reputation",
                                "correct": True,
                            },
                            {"text": "Yes - always take more money", "correct": False},
                            {
                                "text": "Yes - you can cancel existing clients",
                                "correct": False,
                            },
                            {"text": "Flip a coin", "correct": False},
                        ],
                        "explanation": "Overcommitting risks service quality failures. Your reputation is your most valuable asset - protect it over short-term gains.",
                    },
                    {
                        "question": "What builds trust faster in a pet sitting business?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Sending photo updates and being reliable - demonstrating care",
                                "correct": True,
                            },
                            {"text": "Being the cheapest", "correct": False},
                            {"text": "Having fancy equipment", "correct": False},
                            {"text": "Working the fastest", "correct": False},
                        ],
                        "explanation": "Trust comes from communication and reliability. Showing clients their pets are safe and happy builds loyalty faster than low prices.",
                    },
                    {
                        "question": "Three satisfied clients each refer one friend. This is called:",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Word-of-mouth marketing - free customer acquisition",
                                "correct": True,
                            },
                            {"text": "A lucky accident", "correct": False},
                            {"text": "Illegal marketing", "correct": False},
                            {"text": "Network selling", "correct": False},
                        ],
                        "explanation": "Referrals are the most cost-effective marketing. Happy customers become your sales force, bringing new business at zero acquisition cost.",
                    },
                ],
            },
            {
                "title": "School Supplies Store",
                "description": "Master seasonal business dynamics, bulk purchasing, inventory forecasting, and timing-based pricing strategies.",
                "icon": "📚",
                "duration": 90,
                "order": 7,
                "learning_objectives": [
                    "Seasonal demand patterns",
                    "Bulk purchasing and wholesale pricing",
                    "Inventory forecasting",
                    "Competitive pricing in crowded markets",
                    "Managing working capital",
                ],
                "quiz_questions": [
                    {
                        "question": "Why are school supplies most profitable in August (before school starts)?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Peak demand - customers urgently need items and are less price-sensitive",
                                "correct": True,
                            },
                            {
                                "text": "Supplies are cheaper to buy then",
                                "correct": False,
                            },
                            {"text": "It's just tradition", "correct": False},
                            {"text": "Weather is better", "correct": False},
                        ],
                        "explanation": "Seasonal businesses make most profit during peak demand when urgency reduces price sensitivity. Timing is everything.",
                    },
                    {
                        "question": "Buying 100 notebooks at $0.40 each vs. 20 at $0.50 each saves you:",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "$10 through bulk discount ($50 vs. $40 for first 20 units)",
                                "correct": True,
                            },
                            {"text": "$5", "correct": False},
                            {"text": "$20", "correct": False},
                            {"text": "Nothing - same total cost", "correct": False},
                        ],
                        "explanation": "Bulk discounts reduce per-unit costs. Small order: 20 × $0.50 = $10. Bulk: 20 × $0.40 = $8. Savings: $2 per 20 units = $10 for 100 units.",
                    },
                    {
                        "question": "It's late September and school started. You have $200 in unsold inventory. What should you do?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Clearance sale - recover some money rather than hold dead stock",
                                "correct": True,
                            },
                            {"text": "Keep full price and wait", "correct": False},
                            {"text": "Throw it away", "correct": False},
                            {"text": "Increase prices", "correct": False},
                        ],
                        "explanation": "After peak season, demand crashes. Clear inventory at discounts to free up capital - some money is better than dead stock.",
                    },
                    {
                        "question": "Fixed costs (rent) must be paid whether you sell much or little. When are they easiest to cover?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "During peak season when revenue is highest",
                                "correct": True,
                            },
                            {"text": "During slow season", "correct": False},
                            {"text": "They're equally easy anytime", "correct": False},
                            {
                                "text": "Fixed costs don't need to be covered",
                                "correct": False,
                            },
                        ],
                        "explanation": "Seasonal businesses must capture peak demand to cover fixed costs. High revenue periods subsidize the entire operation.",
                    },
                ],
            },
            {
                "title": "Handmade Crafts Online Store",
                "description": "Learn to value your labor, understand e-commerce dynamics, manage production constraints, and build online reputation.",
                "icon": "🎨",
                "duration": 100,
                "order": 8,
                "learning_objectives": [
                    "Production cost calculation (materials + time)",
                    "Pricing handmade goods (value of labor)",
                    "Online marketplace dynamics",
                    "Customer reviews and reputation",
                    "Time as a resource (opportunity cost)",
                ],
                "quiz_questions": [
                    {
                        "question": "A bracelet costs $0.50 in materials and takes 20 minutes. If you value your time at $12/hour, what's the minimum price?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "$4.50 ($0.50 + $4.00 labor + profit margin)",
                                "correct": True,
                            },
                            {"text": "$0.50 - just cover materials", "correct": False},
                            {"text": "$12.50", "correct": False},
                            {"text": "$2.00", "correct": False},
                        ],
                        "explanation": "Calculate: $0.50 materials + (20 min ÷ 60 min × $12/hr) = $0.50 + $4.00 = $4.50 minimum before profit.",
                    },
                    {
                        "question": "Why are online reviews crucial for handmade sellers?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Build trust with strangers - customers can't see items in person",
                                "correct": True,
                            },
                            {"text": "They're legally required", "correct": False},
                            {"text": "They don't actually matter", "correct": False},
                            {"text": "Just for decoration", "correct": False},
                        ],
                        "explanation": "Online purchases require trust. Reviews provide social proof and reduce perceived risk for buyers who can't physically examine products.",
                    },
                    {
                        "question": "You're getting 10 orders per day but each takes 1 hour. You only have 6 hours available. What's the problem?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Capacity constraint - demand exceeds your production ability",
                                "correct": True,
                            },
                            {"text": "You need to work faster only", "correct": False},
                            {"text": "There is no problem", "correct": False},
                            {"text": "Just raise prices randomly", "correct": False},
                        ],
                        "explanation": "Time is your constraint. You must either: increase prices (reduce demand), extend hours, or hire help. You can't serve unlimited customers.",
                    },
                    {
                        "question": "Make-to-order vs. make-to-stock: What's the key tradeoff?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Make-to-order avoids inventory risk but limits speed; stock enables fast shipping but risks unsold items",
                                "correct": True,
                            },
                            {
                                "text": "Make-to-order is always better",
                                "correct": False,
                            },
                            {
                                "text": "Make-to-stock is always better",
                                "correct": False,
                            },
                            {"text": "There's no difference", "correct": False},
                        ],
                        "explanation": "Trade-off: Inventory (capital risk) vs. speed (customer satisfaction). Each model suits different products and markets.",
                    },
                ],
            },
            {
                "title": "Snow Removal Service",
                "description": "Navigate weather uncertainty, understand contracts vs. per-job pricing, manage physical capacity, and handle business risk.",
                "icon": "❄️",
                "duration": 95,
                "order": 9,
                "learning_objectives": [
                    "Weather-dependent business planning",
                    "Equipment investment decisions",
                    "Risk management (weather unpredictability)",
                    "Customer contracts vs. on-demand pricing",
                    "Physical capacity constraints",
                ],
                "quiz_questions": [
                    {
                        "question": "Season contracts ($200 upfront) vs. per-storm pricing ($40/storm). Which is riskier for you?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Contracts - if there are 6+ heavy storms, you work more for same pay",
                                "correct": True,
                            },
                            {
                                "text": "Per-storm - you might not make any money",
                                "correct": False,
                            },
                            {"text": "They're equally risky", "correct": False},
                            {"text": "Neither has any risk", "correct": False},
                        ],
                        "explanation": "Contracts transfer weather risk to you. Heavy snow winter = more work for fixed pay. Per-storm transfers risk to customer.",
                    },
                    {
                        "question": "You can buy a basic shovel ($20) or snow blower ($110). The blower clears driveways 4x faster. When is it worth it?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "If the extra speed lets you serve enough additional customers to recover the $90 difference",
                                "correct": True,
                            },
                            {
                                "text": "Always buy the most expensive equipment",
                                "correct": False,
                            },
                            {
                                "text": "Never - shovels are always better",
                                "correct": False,
                            },
                            {"text": "Just guess randomly", "correct": False},
                        ],
                        "explanation": "ROI calculation: Will increased capacity generate $90+ in additional profit? Equipment is an investment that must pay for itself.",
                    },
                    {
                        "question": "A blizzard hits but you're exhausted from clearing 8 driveways. More customers call. What's the risk of accepting?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Poor service quality from fatigue could damage reputation more than the revenue is worth",
                                "correct": True,
                            },
                            {
                                "text": "No risk - always take more work",
                                "correct": False,
                            },
                            {"text": "You might make too much money", "correct": False},
                            {"text": "Weather might improve", "correct": False},
                        ],
                        "explanation": "Physical businesses have limits. Overextending risks quality failures, injury, and reputation damage - protecting your reputation matters.",
                    },
                    {
                        "question": "Why is being first to clear driveways after a storm valuable?",
                        "type": "multiple",
                        "answers": [
                            {
                                "text": "Customers need service urgently - timing captures demand before competitors",
                                "correct": True,
                            },
                            {"text": "Snow is lighter when fresh", "correct": False},
                            {"text": "It's not valuable", "correct": False},
                            {"text": "You can charge less", "correct": False},
                        ],
                        "explanation": "Time-sensitive services have urgency premiums. Being first means capturing customers before they find alternatives.",
                    },
                ],
            },
        ]

        # Create lessons and quizzes
        for lesson_data in lessons_data:
            lesson, created = Lesson.objects.get_or_create(
                path=path,
                order=lesson_data["order"],
                defaults={
                    "title": lesson_data["title"],
                    "description": lesson_data["description"],
                    "icon": lesson_data["icon"],
                    "duration": lesson_data["duration"],
                    "content": f"<h2>{lesson_data['title']}</h2><h3>Learning Objectives:</h3><ul>{''.join(f'<li>{obj}</li>' for obj in lesson_data['learning_objectives'])}</ul>",
                    "points": 15 + (lesson_data["order"] * 5),
                    "coins": 10 + (lesson_data["order"] * 2),
                    "requires_previous": lesson_data["order"] > 1,
                    "is_active": True,
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"  ✓ Lesson {lesson.order}: {lesson.title}")
                )

                # Create quiz
                quiz = Quiz.objects.create(
                    lesson=lesson,
                    title=f"{lesson.title} - Knowledge Check",
                    description=f"Test your understanding of {lesson.title.lower()} concepts",
                    pass_percentage=75,
                    is_active=True,
                )

                # Create questions
                for idx, q_data in enumerate(lesson_data["quiz_questions"], 1):
                    question = Question.objects.create(
                        quiz=quiz,
                        question_text=q_data["question"],
                        question_type=q_data["type"],
                        points=2,
                        order=idx,
                        explanation=q_data.get("explanation", ""),
                    )

                    for ans_idx, ans_data in enumerate(q_data["answers"], 1):
                        Answer.objects.create(
                            question=question,
                            answer_text=ans_data["text"],
                            is_correct=ans_data["correct"],
                            order=ans_idx,
                        )

                self.stdout.write(
                    f"    ✓ Created quiz with {len(lesson_data['quiz_questions'])} questions"
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"  ⚠ Lesson exists: {lesson.title}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Complete! Created {path.lessons.count()} lessons")
        )
