using UnityEngine;
using UnityEditor;

public static class SpritesHelper
{
    const float CanvasWidth = 24f;
    const float CanvasHeight = 48f;
    static readonly Vector2 CanvasBottomMiddle = new Vector2(CanvasWidth / 2f, CanvasHeight);

    public static void AddPartSprite(GameObject parent, string partName, string pngPath, Rect onCanvas, int drawOrder)
    {
        GameObject partSprite = new GameObject(partName);
        partSprite.transform.SetParent(parent.transform);
        partSprite.transform.localPosition = GetPartPosition(onCanvas);
        SpriteRenderer spriteComponent = partSprite.AddComponent<SpriteRenderer>();
        spriteComponent.sprite = AssetDatabase.LoadAssetAtPath<Sprite>(pngPath);
        spriteComponent.sortingOrder = drawOrder;
    }

    static Vector3 GetPartPosition(Rect part)
    {
        float sideways = part.center.x - CanvasBottomMiddle.x;
        float up = CanvasBottomMiddle.y - part.center.y;
        return new Vector3(sideways, up, 0f);
    }
}