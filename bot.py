#!/usr/bin/env python3
import discord
from discord import app_commands
from discord.ext import commands
from supabase import create_client
from datetime import datetime, date, timedelta
from config import DISCORD_TOKEN, SUPABASE_URL, SUPABASE_KEY

# Initialize bot and database client
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def calculate_credits(consecutive_days):
    """Calculate credits based on consecutive check-in days"""
    if consecutive_days == 1:
        return 5
    elif consecutive_days <= 6:
        return 10
    elif consecutive_days <= 19:
        return 15
    else:
        return 20

def get_user_stats(user_id):
    """Get user's total credits and consecutive days from existing check-in records
    
    Example: User checked in on days 1,2,3,5,6,7
    - Days 1,2,3: streak of 3 days -> 5+10+10 = 25 credits
    - Day 5: new streak starts -> 5 credits  
    - Days 6,7: continue streak -> 10+10 = 20 credits
    - Total: 25+5+20 = 50 credits
    - Current consecutive: 3 days (if today is day 8 or yesterday was day 7)
    """
    try:
        # Get all user check-ins ordered by date
        result = supabase.table('user_sign_ins').select('*').eq('user_id', user_id).order('sign_in_time').execute()
        
        if not result.data:
            return 0, 0  # total_credits, consecutive_days
        
        # Convert to dates and sort
        check_in_dates = []
        for record in result.data:
            try:
                # Handle different datetime formats
                time_str = record['sign_in_time']
                print(f"Debug: Parsing time string: {time_str}")
                
                # Remove microseconds if present and handle timezone
                if '.' in time_str and '+' in time_str:
                    # Format: 2025-08-02T16:45:58.86854+00:00
                    time_str = time_str.split('.')[0] + '+00:00'
                elif 'Z' in time_str:
                    # Format: 2025-08-02T16:45:58Z
                    time_str = time_str.replace('Z', '+00:00')
                
                if 'T' in time_str:
                    record_date = datetime.fromisoformat(time_str).date()
                else:
                    record_date = datetime.fromisoformat(time_str).date()
                
                print(f"Debug: Parsed date: {record_date}")
                check_in_dates.append(record_date)
            except Exception as e:
                print(f"Debug: Failed to parse {time_str}: {e}")
                continue
        
        # Remove duplicates and sort
        unique_dates = sorted(list(set(check_in_dates)))
        
        if not unique_dates:
            return 0, 0
        
        print(f"Debug: Found {len(unique_dates)} unique check-in dates for user {user_id}")
        
        # Calculate total credits based on all check-ins with proper streak calculation
        # Each streak is calculated independently and all credits are accumulated
        total_credits = 0
        current_streak = 0
        last_date = None
        
        for check_date in unique_dates:
            if last_date is None:
                # First check-in ever
                current_streak = 1
            elif check_date == last_date + timedelta(days=1):
                # Consecutive day - continue streak
                current_streak += 1
            else:
                # Gap in days - start new streak
                current_streak = 1
            
            credits_for_day = calculate_credits(current_streak)
            total_credits += credits_for_day
            last_date = check_date
            
            print(f"Debug: Date {check_date}, Streak: {current_streak}, Credits: {credits_for_day}")
            
        print(f"Debug: Total credits calculated: {total_credits}")
        
        # Calculate current consecutive days (from most recent date backwards)
        today = date.today()
        consecutive_days = 0
        
        # Check if user has recent check-ins for current streak
        latest_date = unique_dates[-1]
        if latest_date == today or latest_date == today - timedelta(days=1):
            consecutive_days = 1
            check_date = latest_date - timedelta(days=1)
            
            # Count backwards to find consecutive streak
            for i in range(len(unique_dates) - 2, -1, -1):
                if unique_dates[i] == check_date:
                    consecutive_days += 1
                    check_date -= timedelta(days=1)
                else:
                    break
        else:
            # Streak is broken, but user still has total credits
            consecutive_days = 0
        
        print(f"Debug: Current consecutive days: {consecutive_days}")
        
        return total_credits, consecutive_days
    except Exception as e:
        print(f"Debug: Error in get_user_stats: {e}")
        return 0, 0

@bot.event
async def on_ready():
    print(f'✅ {bot.user} connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} slash commands')
    except Exception as e:
        print(f'❌ Failed to sync slash commands: {e}')

@bot.tree.command(name='blast', description='Daily check-in - Each user can only check in once per day')
async def blast(interaction: discord.Interaction):
    """Daily check-in command - Each user can only check in once per day"""
    try:
        user_id = str(interaction.user.id)
        username = interaction.user.name
        today = date.today().isoformat()
        
        # Check if user already checked in today
        result = supabase.table('user_sign_ins').select('*').eq('user_id', user_id).gte('sign_in_time', f'{today}T00:00:00').execute()
        
        if result.data:
            await interaction.response.send_message(f'⚠️ **{username}** You have already checked in today! Come back tomorrow~')
            return
        
        # Calculate consecutive days and credits
        total_credits, current_consecutive = get_user_stats(user_id)
        
        # Check if yesterday was checked in to determine new consecutive days
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        yesterday_result = supabase.table('user_sign_ins').select('*').eq('user_id', user_id).gte('sign_in_time', f'{yesterday}T00:00:00').lt('sign_in_time', f'{today}T00:00:00').execute()
        
        if yesterday_result.data:
            # Consecutive check-in
            new_consecutive_days = current_consecutive + 1
        else:
            # First check-in or break in streak
            new_consecutive_days = 1
        
        # Calculate credits for today
        today_credits = calculate_credits(new_consecutive_days)
        
        # Perform check-in
        data = {
            'user_id': user_id,
            'username': username,
            'sign_in_time': datetime.now().isoformat()
        }
        
        supabase.table('user_sign_ins').insert(data).execute()
        
        # Create response embed
        embed = discord.Embed(
            title="✅ Check-in Successful!",
            description=f"**{username}** has checked in successfully!",
            color=discord.Color.green()
        )
        embed.add_field(name="Credits Earned", value=f"+{today_credits} credits", inline=True)
        embed.add_field(name="Consecutive Days", value=f"{new_consecutive_days} days", inline=True)
        embed.add_field(name="Total Credits", value=f"{total_credits + today_credits} credits", inline=True)
        embed.set_footer(text="Keep the streak going! 🔥")
        
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        await interaction.response.send_message(f'❌ Check-in failed: {e}')

@bot.tree.command(name='credit', description='Check your total credits and consecutive check-in days')
async def credit(interaction: discord.Interaction):
    """Check user's credit stats and consecutive days"""
    try:
        user_id = str(interaction.user.id)
        username = interaction.user.name
        
        # Get user stats
        total_credits, consecutive_days = get_user_stats(user_id)
        
        # Also check if user has any check-ins at all
        result = supabase.table('user_sign_ins').select('*').eq('user_id', user_id).execute()
        has_checkins = len(result.data) > 0
        
        if not has_checkins:
            embed = discord.Embed(
                title="💰 Your Credits",
                description=f"**{username}**, you haven't checked in yet!",
                color=discord.Color.orange()
            )
            embed.add_field(name="Total Credits", value="0 credits", inline=True)
            embed.add_field(name="Consecutive Days", value="0 days", inline=True)
            embed.add_field(name="Next Reward", value="5 credits for first check-in", inline=False)
            embed.set_footer(text="Use /blast to start your check-in streak!")
        else:
            # Calculate next day's credits
            next_credits = calculate_credits(consecutive_days + 1)
            
            embed = discord.Embed(
                title="💰 Your Credits",
                description=f"**{username}**'s check-in statistics",
                color=discord.Color.gold()
            )
            embed.add_field(name="Total Credits", value=f"{total_credits} credits", inline=True)
            embed.add_field(name="Consecutive Days", value=f"{consecutive_days} days", inline=True)
            embed.add_field(name="Next Reward", value=f"{next_credits} credits", inline=True)
            
            # Add streak info
            if consecutive_days >= 20:
                streak_status = "🔥 Maximum streak! 20 credits daily"
            elif consecutive_days >= 7:
                streak_status = f"🚀 Great streak! {20 - consecutive_days} more days for max reward"
            elif consecutive_days >= 2:
                streak_status = f"📈 Building streak! {7 - consecutive_days} more days for 15 credits"
            else:
                streak_status = "🌱 Just getting started!"
            
            embed.add_field(name="Streak Status", value=streak_status, inline=False)
            embed.set_footer(text="Keep checking in daily to maintain your streak! 🔥")
        
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        await interaction.response.send_message(f'❌ Failed to get credit info: {e}')

@bot.tree.command(name='debug', description='Debug user check-in data (admin only)')
async def debug(interaction: discord.Interaction):
    """Debug command to check user's raw data"""
    try:
        user_id = str(interaction.user.id)
        
        # Get raw data
        result = supabase.table('user_sign_ins').select('*').eq('user_id', user_id).order('sign_in_time').execute()
        
        debug_info = f"**Debug Info for {interaction.user.name}**\n"
        debug_info += f"User ID: {user_id}\n"
        debug_info += f"Total records: {len(result.data)}\n\n"
        
        if result.data:
            debug_info += "**Raw Records:**\n"
            for i, record in enumerate(result.data):
                debug_info += f"{i+1}. {record['sign_in_time']}\n"
            
            # Test the calculation
            total_credits, consecutive_days = get_user_stats(user_id)
            debug_info += f"\n**Calculated Results:**\n"
            debug_info += f"Total Credits: {total_credits}\n"
            debug_info += f"Consecutive Days: {consecutive_days}\n"
        else:
            debug_info += "No records found!\n"
        
        await interaction.response.send_message(f"```{debug_info}```")
        
    except Exception as e:
        await interaction.response.send_message(f'❌ Debug failed: {e}')

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)