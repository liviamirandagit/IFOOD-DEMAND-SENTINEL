package com.ifood;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class searchEvent {
    private String userId;
    private String searchQuery;
    private double latitude;
    private double longitude;
    private String h3Index;
}