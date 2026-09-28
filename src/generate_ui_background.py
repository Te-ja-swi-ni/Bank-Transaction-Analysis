import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_dashboard_background():
    # Setup the figure (16:9 aspect ratio standard for Power BI)
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor('#0D1117') # GitHub Dark Dimmed background
    ax.set_facecolor('#0D1117')
    ax.axis('off')

    # Accent Header Line
    header_line = patches.Rectangle((0, 8.8), 16, 0.1, fill=True, color='#00C49F', alpha=0.8)
    ax.add_patch(header_line)
    
    # Title Area
    plt.text(0.5, 8.3, "Bank Transaction Desktop Analytics", color="#ffffff", fontsize=28, fontweight='bold', alpha=0.9, fontfamily='sans-serif')
    plt.text(0.5, 7.9, "Interactive Descriptive Dashboard | Phase 7 Operations Model", color="#8B949E", fontsize=14, fontfamily='sans-serif')

    # Draw KPI Card boxes (Top Row)
    kpi_y = 6.4
    kpi_height = 1.2
    kpi_width = 3.5
    for i in range(4):
        x = 0.5 + (i * 3.8)
        rect = patches.FancyBboxPatch((x, kpi_y), kpi_width, kpi_height,
                                      boxstyle="round,pad=0.1,rounding_size=0.1",
                                      fill=True, color='#161B22', ec='#30363D', lw=1.5, alpha=0.95)
        ax.add_patch(rect)

    # Draw Main Visual Boxes (Middle and Bottom)
    # Left Slicer Panel
    left_panel = patches.FancyBboxPatch((0.5, 0.5), 2.5, 5.5,
                                  boxstyle="round,pad=0.1,rounding_size=0.1",
                                  fill=True, color='#161B22', ec='#30363D', lw=1.5, alpha=0.95)
    ax.add_patch(left_panel)

    # Middle Main Chart
    middle_chart = patches.FancyBboxPatch((3.3, 3.2), 8.5, 2.8,
                                  boxstyle="round,pad=0.1,rounding_size=0.1",
                                  fill=True, color='#161B22', ec='#30363D', lw=1.5, alpha=0.95)
    ax.add_patch(middle_chart)
    
    # Bottom Wide Chart
    bottom_chart = patches.FancyBboxPatch((3.3, 0.5), 12.0, 2.4,
                                  boxstyle="round,pad=0.1,rounding_size=0.1",
                                  fill=True, color='#161B22', ec='#30363D', lw=1.5, alpha=0.95)
    ax.add_patch(bottom_chart)

    # Right Side Chart
    right_chart = patches.FancyBboxPatch((12.1, 3.2), 3.2, 2.8,
                                  boxstyle="round,pad=0.1,rounding_size=0.1",
                                  fill=True, color='#161B22', ec='#30363D', lw=1.5, alpha=0.95)
    ax.add_patch(right_chart)

    # Subtle glowing orbs in the background for aesthetic
    circle1 = patches.Circle((2, 8), radius=2, color='#00C49F', alpha=0.03, zorder=0)
    circle2 = patches.Circle((14, 2), radius=3, color='#FFBB28', alpha=0.02, zorder=0)
    ax.add_patch(circle1)
    ax.add_patch(circle2)

    # Save format
    os.makedirs('outputs/powerbi_data', exist_ok=True)
    out_path = 'outputs/powerbi_data/Dashboard_Background.png'
    plt.xlim(0, 16)
    plt.ylim(0, 9)
    plt.savefig(out_path, facecolor=fig.get_facecolor(), bbox_inches='tight', pad_inches=0.0)
    print(f"Generated UI Wireframe Background: {out_path}")

create_dashboard_background()
