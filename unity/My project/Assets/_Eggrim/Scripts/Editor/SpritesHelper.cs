using UnityEngine;
using UnityEditor;

public static class SpritesHelper
{
    public static Vector2 AnchorBottomMiddle(float canvasWidth, float canvasHeight)
    {
        return new Vector2(canvasWidth / 2f, canvasHeight);
    }

    public static void AddPartSprite(GameObject parent, string partName, string pngPath, Rect onCanvas, Vector2 anchor, int drawOrder, bool flipX)
    {
        GameObject partSprite = new GameObject(partName);
        partSprite.transform.SetParent(parent.transform);
        partSprite.transform.localPosition = GetPartPosition(onCanvas, anchor, flipX);
        SpriteRenderer spriteComponent = partSprite.AddComponent<SpriteRenderer>();
        spriteComponent.sprite = AssetDatabase.LoadAssetAtPath<Sprite>(pngPath);
        spriteComponent.flipX = flipX;
        spriteComponent.sortingOrder = drawOrder;
    }

    static Vector3 GetPartPosition(Rect part, Vector2 anchor, bool flipX)
    {
        float sideways = part.center.x - anchor.x;
        if (flipX) sideways = -sideways;
        float up = anchor.y - part.center.y;
        return new Vector3(sideways, up, 0f);
    }
}