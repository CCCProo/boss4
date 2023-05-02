@bot.on.message(text=["Босс"])
async def button_handler(message: Message):
	from_id=message.from_id
	REGISTER(from_id)
	with open(f"boss/mulim.json", "r") as file:
		mulim_info = json.load(file)
	keyboard = Keyboard(inline=True)
	keyboard.add(Text("⚔ Атаковать",payload={"cmd": "attack_mulim"}), color=KeyboardButtonColor.POSITIVE)
	keyboard.row()
	keyboard.add(Text("📄 Список игроков по урону",payload={"cmd": "table_mulim"}), color=KeyboardButtonColor.POSITIVE)
	keyboard.row()
	keyboard.add(Text(f"💰 Награды по урону", {"cmd": "yron_mulim"}),color=KeyboardButtonColor.NEGATIVE)
	if 1500000 >= mulim_info['XP']:
		xp = "{:,}".format(mulim_info['XP'])
	else:
		xp = "{:,}".format(1500000)
	await message.answer(f"""⚔ Мировой босс: Милим Нава:

♥ Здоровье: {xp} ♥
✊ Урон: 140 🗡
🔮 Маг.урон: 50 - 60 🔮
🎯 Способность «Чёрная дыра удара»: С шансом 5% может заблокировать весь ваш урон или Маг.урон.
«Регенерация»: С шансом 1% может восстановить какое то количетсво здоровья
🕒 Респаун: 12 часов

🏹 Ваши харатеристики: 1,664 ♥, 438 🗡, 128 🔮

🎒 Дропы:
— 🔷 5,250 🟡, +2000 ⭐ ~100%
— 🔷 +75 🛢 ~80%
— 🔷 Магический слиток (1 - 3 шт) ~55%
— 🔷 Кровь (2 - 4 шт) ~30%
— 🔷 Эссенция души (3 шт) ~30%
— 🔷 Звездная пыль (2-3 шт) ~5%
— 🔷 Чёрная дыра (1 шт) ~1%
""",keyboard=keyboard)

@bot.on.message(payload={"cmd": "table_mulim"})
async def button_handler(message: Message):
    from_id = message.from_id
    REGISTER(from_id)
    with open(f"boss/all_attack_mulim.json", "r") as file:
        all_attack = json.load(file)

    # сортируем словарь по значениям
    sorted_leaderboard = dict(sorted(all_attack.items(), key=lambda item: item[1], reverse=True))
    values_num = 0
    # выводим таблицу лидеров
    all_leader = ""
    with open(f"boss/prize_mulim.json", "r") as file:
        prize_mulim = json.load(file)
    for key, value in sorted_leaderboard.items():
        values_num += 1
        with open(f"my_info/{key}.json", "r") as file:
            my_info = json.load(file)
        with open(f"all_id.json", "r") as file:
            all_id = json.load(file)
        user = await bot.api.users.get(int(key))
        first_name = user[0].first_name

        gems = ""
        for prize_value, prize_gems in prize_mulim.items():
            if value >= int(prize_value):
                gems = f"| {prize_gems} 💎"
                if int(prize_value) <= 650000:
                    bonus_gems = int((value - int(prize_value)) * 0.0002)
                    if bonus_gems > 0:
                        gems += f"(+{bonus_gems}💎)"
                break
        all_leader += f"{values_num}. @id{key}({first_name})[{my_info['Уровень']}] ID: {all_id[str(key)]} — {value} 🗡{gems}\n"
    await message.answer(f"📄 Список игроков по урону на Милим:\n\n{all_leader}")

@bot.on.message(payload={"cmd": "yron_mulim"})
async def button_handler(message: Message):
		from_id = message.from_id
		REGISTER(from_id)
		with open(f"boss/prize_mulim.json", "r") as file:
			prize_mulim = json.load(file)
		text = ""
		for a, b in prize_mulim.items():
			attack =  "{:,}".format(int(a))
			text += f"{attack} 🗡 — {b} 💎\n"
		await message.answer(f"💰 Награды по урону у Милим:\n\n💰 Если вы набрали урона выше максимума, то в размере 0.05% будет расчитываться доп.награда от вашего текущего урона\n\n{text}")


@bot.on.message(payload={"cmd": "attack_mulim"})
async def button_handler(message: Message):
	from_id=message.from_id
	REGISTER(from_id)
	with open(f"boss/mulim.json", "r") as file:
		mulim_info = json.load(file)
	with open(f"boss/prize_mulim.json", "r") as file:
		prize = json.load(file)
	with open(f"boss/all_attack_mulim.json", "r") as file:
		all_attack = json.load(file)
	with open(f"my_info/{from_id}.json", "r") as file:
		my_info = json.load(file)
	my_xp = my_info['Здоровье'] 
	now = int(time.time())
	xul = False
	times = mulim_info['time']
	Krit_True = False
	text_krit = ""
	krit_sh = random.randint(1, 100)
	if my_info["Крит-шанс"] >= krit_sh:
		Krit_True = True
	else:
		Krit_True = False
	krit_value = my_info["Крит-урон"].split(',')
	lower, upper = int(krit_value[0]), int(krit_value[1])
	krit_yron = random.randint(lower, upper)
	
	total_seconds = times - now
	hours = total_seconds // 3600 # целое количество часов
	minutes = (total_seconds % 3600) // 60  # целое количество минут
	seconds = total_seconds % 60   # остаток секунд
	if now <= mulim_info['time']:
		await message.answer(f"❌ Атаковать Милим  можете через {hours} час. {minutes} мин. {seconds} сек.")
	else:
		if my_xp - 150 <= 0:
			xul = True
			await message.answer("❌ Вы погибли. Ожидайте, когда вы вылечитесь")
		else:
			if Krit_True == True:
				my_attack = krit_yron
				text_krit = "❗"
				dop_attack = krit_yron
			else:
				my_attack = my_info['Атака'] + my_info['Маг-Урон']
			if mulim_info['XP'] - my_attack  <= 0:
				#добавишь сам добавление наград если что
				mulim_info['XP'] = 1500000
				mulim_info['time'] = now + 43200
								
				await message.answer(f"Милим убита")
			else:
				black_hole = False
				xul = False
				Regen = False
				random_spop = round(random.uniform(1.0, 100.0), 2)	
				yvorot_rand = random.randint(1, 100)
				boss_xp = mulim_info['XP']
				yvorod_text = ""
				form_boss_xp = "{:,}".format(boss_xp - my_attack)
				keyboard = Keyboard(inline=True)
				keyboard.add(Text(f"⚔ Атаковать ({form_boss_xp} ♥)",payload={"cmd": "attack_mulim"}), color=KeyboardButtonColor.POSITIVE)
				keyboard.row()		
				
				if yvorot_rand <= my_info['Уворот']:
					yvorod = True
				else:
					yvorod = False
				if yvorod == True:
					attack_mob = 0
					yvorod_text = "| 💫 Уворот"
				else:
					attack_mob = random.randint(140, 150)
				keyboard.add(Callback(f"♥ Твое здоровье ({my_xp - attack_mob} ♥)",payload={"cmd": "MY_XP_NONE"}),color=KeyboardButtonColor.NEGATIVE),
				if random_spop <= 5:
					black_hole = True
					Regen = False
				if random_spop <= 1.5:
					black_hole = False
					Regen = True
				if black_hole == True:
					text_all = ""
					rand50_50 = random_spop = random.randint(1, 100)
					if rand50_50 <= 30:
						Yron = True
						text_all = f"Милим блокировала вашу маг.атаку {yvorod_text}"
						my_attack = my_info['Атака'] + dop_attack
					else:
						Yron = False
						text_all = f"Милим блокировала вашу атаку {yvorod_text}"
						my_attack =  my_info['Маг-Урон']
					await message.answer(f"🎯 Милим использовала способность «Чёрная дыра удара». {text_all}\n\n🎽 Вы ударили по Милим {my_attack} {text_krit}",keyboard=keyboard)
				elif Regen == True:
					if yvorod == True:
						yvorod_text = "| 💫 Уворот"
					regent_rand = random.randint(900, 12000)	
					my_attack = 0
					form_boss_xp = "{:,}".format(boss_xp + regent_rand)
					keyboard = Keyboard(inline=True)
					keyboard.add(Text(f"⚔ Атаковать ({form_boss_xp} ♥)",payload={"cmd": "attack_mulim"}), color=KeyboardButtonColor.POSITIVE)
					keyboard.row()		
					keyboard.add(Callback(f"♥ Твое здоровье ({my_xp - attack_mob} ♥)",payload={"cmd": "MY_XP_NONE"}),color=KeyboardButtonColor.NEGATIVE),
					await message.answer(f"🎯 Милим использовала способность «Регенерация». Милим восстановила {regent_rand} здоровья ❤ {yvorod_text}.",keyboard=keyboard)
				
					mulim_info['XP'] += regent_rand
					with open(f"boss/mulim.json", "w") as file:
						json.dump(mulim_info, file, ensure_ascii=False, indent=2)
				else:
					if yvorod == True:
						yvorod_text = "| 💫 Уворот"
					await message.answer(f"🦹‍♂ Милим нанесла вам {attack_mob} 🗡 {yvorod_text}\n\n🎽 Вы ударили по Милим {my_attack} {text_krit} 🗡",keyboard=keyboard)
				if str(from_id) in all_attack:
					all_attack[str(from_id)] +=  my_attack
				else:
					all_attack[str(from_id)] =  my_attack
				with open(f"boss/all_attack_mulim.json", "w") as file:
					json.dump(all_attack, file, ensure_ascii=False, indent=2)
				my_info['Здоровье'] -= attack_mob
				mulim_info['XP'] -= my_attack
			my_info['Хил'] = xul
			with open(f"boss/mulim.json", "w") as file:
				json.dump(mulim_info, file, ensure_ascii=False, indent=2)
				with open(f"my_info/{from_id}.json", "w") as file:
					json.dump(my_info, file, ensure_ascii=False, indent=2)
