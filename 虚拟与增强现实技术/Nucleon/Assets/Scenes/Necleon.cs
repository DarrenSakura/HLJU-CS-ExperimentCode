using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class Necleon : MonoBehaviour
{
    public float attractionForce;
    Rigidbody body;
    void Awake()
    {
        body = GetComponent<Rigidbody>();
    }
    void FixedUpdate()
    {
        body.AddForce(transform.localPosition * -attractionForce);
    }
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }
}
