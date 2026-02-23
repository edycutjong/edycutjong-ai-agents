from agent.models import WorkoutPlan
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Workout Plan', 0, 1, 'C')

def export_to_markdown(plan: WorkoutPlan, filename: str):
    """Exports the workout plan to a Markdown file."""
    with open(filename, 'w') as f:
        f.write(f"# {plan.plan_name}\n\n")
        f.write(f"**Difficulty Progression:** {plan.difficulty_progression}\n\n")
        f.write(f"**Equipment Needed:** {', '.join(plan.equipment_needed)}\n\n")

        for week in plan.weeks:
            f.write(f"## Week {week.week_number}: {week.focus}\n\n")
            for session in week.sessions:
                f.write(f"### {session.day}: {session.workout_type}\n")
                f.write(f"- **Duration:** {session.duration_minutes} min\n")
                f.write(f"- **Calories:** ~{session.estimated_calories} kcal\n\n")

                f.write("**Warm-up:**\n")
                for item in session.warm_up:
                    f.write(f"- {item}\n")
                f.write("\n")

                f.write("**Main Workout:**\n")
                for ex in session.main_workout:
                    line = f"- **{ex.name}**: {ex.sets or 'N/A'} sets x {ex.reps or 'N/A'} reps"
                    if ex.duration:
                        line += f" ({ex.duration})"
                    if ex.notes:
                        line += f" - *{ex.notes}*"
                    f.write(f"{line}\n")
                f.write("\n")

                f.write("**Cool-down:**\n")
                for item in session.cool_down:
                    f.write(f"- {item}\n")
                f.write("\n---\n\n")

def export_to_pdf(plan: WorkoutPlan, filename: str):
    """Exports the workout plan to a PDF file."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"{plan.plan_name}", ln=True, align='C')
    pdf.ln(5)

    # Metadata
    pdf.set_font("Arial", size=10)

    # Use multi_cell for potentially long text to avoid overflow, but sanitize input first
    # encode('latin-1', 'replace').decode('latin-1') handles unicode chars not supported by core fonts
    def clean_text(text):
        return text.encode('latin-1', 'replace').decode('latin-1')

    pdf.multi_cell(0, 6, clean_text(f"Difficulty Progression: {plan.difficulty_progression}"))
    pdf.multi_cell(0, 6, clean_text(f"Equipment Needed: {', '.join(plan.equipment_needed)}"))
    pdf.ln(5)

    for week in plan.weeks:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, clean_text(f"Week {week.week_number}: {week.focus}"), ln=True)
        pdf.ln(2)

        for session in week.sessions:
            pdf.set_font("Arial", 'B', 11)
            header_text = f"{session.day}: {session.workout_type} ({session.duration_minutes} min, ~{session.estimated_calories} kcal)"
            pdf.cell(0, 8, clean_text(header_text), ln=True)

            # Warm-up
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 6, "Warm-up:", ln=True)
            pdf.set_font("Arial", size=10)
            for item in session.warm_up:
                pdf.cell(10) # Indent
                pdf.cell(0, 5, clean_text(f"- {item}"), ln=True)

            # Main Workout
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 6, "Main Workout:", ln=True)
            pdf.set_font("Arial", size=10)
            for ex in session.main_workout:
                text = f"- {ex.name}: {ex.sets or 'N/A'} sets x {ex.reps or 'N/A'} reps"
                if ex.duration:
                    text += f" ({ex.duration})"
                if ex.notes:
                    text += f" - {ex.notes}"
                pdf.cell(10) # Indent
                pdf.multi_cell(0, 5, clean_text(text))

            # Cool-down
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 6, "Cool-down:", ln=True)
            pdf.set_font("Arial", size=10)
            for item in session.cool_down:
                pdf.cell(10) # Indent
                pdf.cell(0, 5, clean_text(f"- {item}"), ln=True)

            pdf.ln(3) # Space between sessions

        pdf.add_page() # New page per week usually, or just break if full? Let's add page for clarity.
        # Actually, adding page for every week might be too much if weeks are short.
        # But for a workout plan, it's nice.

    pdf.output(filename)
