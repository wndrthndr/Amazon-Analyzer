import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV
df = pd.read_csv("soft_toys_all.csv")

# Basic Cleaning
df.drop_duplicates(inplace=True)
df.dropna(subset=['Brand', 'Rating', 'Price'], inplace=True)

# Ensure numeric columns are correct
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df.dropna(subset=['Rating', 'Reviews', 'Price'], inplace=True)

# =========================
# 📊 BRAND PERFORMANCE
# =========================

# Brand Frequency
top_brands = df['Brand'].value_counts().nlargest(5)

plt.figure(figsize=(8, 4))
sns.barplot(x=top_brands.index, y=top_brands.values, palette="viridis")
plt.title("Top 5 Brands by Frequency")
plt.xlabel("Brand")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("plots/brand_frequency.png")
plt.close()

# Average Rating by Brand
avg_rating_by_brand = df.groupby('Brand')['Rating'].mean().sort_values(ascending=False).head(5)

plt.figure(figsize=(8, 4))
sns.barplot(x=avg_rating_by_brand.index, y=avg_rating_by_brand.values, palette="coolwarm")
plt.title("Top 5 Brands by Average Rating")
plt.xlabel("Brand")
plt.ylabel("Avg Rating")
plt.tight_layout()
plt.savefig("plots/brand_rating.png")
plt.close()

# Pie Chart of Brand Share
plt.figure(figsize=(6, 6))
top_brands.plot.pie(autopct='%1.1f%%', startangle=90, cmap='Set3')
plt.title("Brand Share of Top 5")
plt.ylabel("")
plt.tight_layout()
plt.savefig("plots/brand_share_pie.png")
plt.close()

# =========================
# 💸 PRICE VS RATING
# =========================

plt.figure(figsize=(8, 5))
sns.scatterplot(x='Rating', y='Price', data=df, hue='Brand', legend=False)
plt.title("Price vs Rating")
plt.xlabel("Rating")
plt.ylabel("Price (INR)")
plt.tight_layout()
plt.savefig("plots/price_vs_rating.png")
plt.close()

# Average Price by Rating Buckets
df['Rating Bucket'] = pd.cut(df['Rating'], bins=[0, 2, 3, 4, 5], labels=['0-2', '2-3', '3-4', '4-5'])

price_by_rating = df.groupby('Rating Bucket')['Price'].mean()

plt.figure(figsize=(8, 4))
sns.barplot(x=price_by_rating.index, y=price_by_rating.values, palette="YlGnBu")
plt.title("Average Price by Rating Range")
plt.xlabel("Rating Range")
plt.ylabel("Avg Price (INR)")
plt.tight_layout()
plt.savefig("plots/avg_price_by_rating.png")
plt.close()

# =========================
# 🌟 TOP PRODUCTS
# =========================

# Most Reviewed Products
top_reviewed = df.sort_values(by='Reviews', ascending=False).head(5)

plt.figure(figsize=(10, 4))
sns.barplot(x=top_reviewed['Title'].str[:30], y=top_reviewed['Reviews'], palette="magma")
plt.title("Top 5 Most Reviewed Products")
plt.xlabel("Product Title")
plt.ylabel("Reviews")
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig("plots/top_reviewed.png")
plt.close()

# Top Rated Products
top_rated = df[df['Reviews'] > 10].sort_values(by='Rating', ascending=False).head(5)

plt.figure(figsize=(10, 4))
sns.barplot(x=top_rated['Title'].str[:30], y=top_rated['Rating'], palette="plasma")
plt.title("Top 5 Highest Rated Products (with >10 reviews)")
plt.xlabel("Product Title")
plt.ylabel("Rating")
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig("plots/top_rated.png")
plt.close()

print("✅ Analysis complete. Graphs saved in /plots folder.")
