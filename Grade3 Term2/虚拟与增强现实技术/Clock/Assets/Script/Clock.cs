using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Clock : MonoBehaviour
{
    public Transform Hourprovit;
    public Transform Minuteprovit;
    public Transform Secondprovit;
    // Start is called before the first frame update
    void Start()
    {
        //System.DateTime now;
    }

    // Update is called once per frame
    void Update()
    {
        Hourprovit.localRotation = Quaternion.Euler(0, 30 * System.DateTime.Now.Hour, 0);
        Minuteprovit.localRotation = Quaternion.Euler(0, 6 * System.DateTime.Now.Minute, 0);
        Secondprovit.localRotation = Quaternion.Euler(0, 6 * System.DateTime.Now.Second, 0);
    }
}