import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load raw scraped data
if not os.path.exists("soft_toys_all.csv"):
    print("❌ File 'sponsored_soft_toys.csv' not found. Please run the scraper first.")
    exit()

df = pd.read_csv("soft_toys_all.csv")

print("🔧 Cleaning data...")
# Drop rows with missing critical fields
df.dropna(subset=["Price", "Rating", "Reviews", "Brand"], inplace=True)

# Convert to numeric
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")

# Drop any remaining invalid rows
df.dropna(subset=["Price", "Rating", "Reviews"], inplace=True)

# Save cleaned file
df.to_csv("cleaned_soft_toys.csv", index=False)
print("✅ Cleaned data saved to 'cleaned_soft_toys.csv'.")

# Start Analysis
print("📊 Starting analysis...")

# ========== Brand Performance Analysis ==========
top_brands = df['Brand'].value_counts().head(5)

plt.figure(figsize=(8, 5))
sns.barplot(x=top_brands.index, y=top_brands.values, palette='pastel')
plt.title("Top 5 Brands by Frequency")
plt.xlabel("Brand")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("brand_frequency_bar.png")
plt.close()

plt.figure(figsize=(6, 6))
top_brand_percent = top_brands / top_brands.sum()
plt.pie(top_brand_percent, labels=top_brand_percent.index, autopct='%1.1f%%', startangle=140)
plt.title("Brand Share (Top 5)")
plt.savefig("brand_share_pie.png")
plt.close()

print("✅ Brand analysis done. Saved 'brand_frequency_bar.png' and 'brand_share_pie.png'.")

# ========== Price vs Rating ==========
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Rating", y="Price", hue="Brand", alpha=0.6)
plt.title("Price vs Rating (Colored by Brand)")
plt.tight_layout()
plt.savefig("price_vs_rating_scatter.png")
plt.close()

# Average Price by Rating Range
df["Rating Range"] = pd.cut(df["Rating"], bins=[0, 2, 3, 4, 5], labels=["0-2", "2-3", "3-4", "4-5"])
avg_price_by_rating = df.groupby("Rating Range")["Price"].mean()

plt.figure(figsize=(8, 5))
sns.barplot(x=avg_price_by_rating.index, y=avg_price_by_rating.values, palette="coolwarm")
plt.title("Average Price by Rating Range")
plt.xlabel("Rating Range")
plt.ylabel("Average Price")
plt.tight_layout()
plt.savefig("avg_price_by_rating.png")
plt.close()

print("✅ Price vs Rating analysis done. Saved 'price_vs_rating_scatter.png' and 'avg_price_by_rating.png'.")

# ========== Review & Rating Distribution ==========
top_by_reviews = df.sort_values(by="Reviews", ascending=False).head(5)
top_by_rating = df.sort_values(by="Rating", ascending=False).head(5)

plt.figure(figsize=(10, 5))
sns.barplot(data=top_by_reviews, x="Title", y="Reviews", palette="viridis")
plt.title("Top 5 Products by Reviews")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("top_products_by_reviews.png")
plt.close()

plt.figure(figsize=(10, 5))
sns.barplot(data=top_by_rating, x="Title", y="Rating", palette="plasma")
plt.title("Top 5 Products by Rating")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("top_products_by_rating.png")
plt.close()

print("✅ Review/Rating distribution analysis complete. Saved 'top_products_by_reviews.png' and 'top_products_by_rating.png'.")

print("\n🎉 All analysis complete. Check your folder for cleaned CSV + visualizations.")
